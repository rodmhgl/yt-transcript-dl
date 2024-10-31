#!/usr/bin/env python3

import sys
import argparse
import pyperclip
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from typing import List, Dict
import re
import json
from datetime import timedelta

def get_video_id(url_or_id: str) -> str:
    """
    Extract video ID from URL or return the ID if it's already just the ID.
    
    Args:
        url_or_id (str): YouTube URL or video ID

    Returns:
        str: YouTube video ID

    Raises:
        ValueError: If the input is not a valid YouTube URL or video ID
    """
    # Match patterns like youtube.com/watch?v=XXX or youtu.be/XXX
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL or video ID")

def get_transcript(video_id: str) -> List[Dict]:
    """
    Fetch transcript from YouTube video.
    
    Args:
        video_id (str): YouTube video ID

    Returns:
        List[Dict]: List of transcript entries

    Raises:
        Exception: If transcript cannot be fetched
    """
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}", file=sys.stderr)
        sys.exit(1)

def format_transcript(transcript: List[Dict], format_type: str = 'text', 
                     include_timestamps: bool = False) -> str:
    """
    Format transcript with or without timestamps.
    
    Args:
        transcript (List[Dict]): List of transcript entries
        include_timestamps (bool): Whether to include timestamps in output

    Returns:
        str: Formatted transcript text
    """
    if format_type == 'text':
        if include_timestamps:
            formatted_lines = []
            for entry in transcript:
                formatted_lines.append(f"{format_timestamp(entry)} {entry['text']}")
            return "\n".join(formatted_lines)
        else:
            formatter = TextFormatter()
            return formatter.format_transcript(transcript)
            
    elif format_type == 'json':
        # Convert to JSON with formatted timestamps
        json_transcript = []
        for entry in transcript:
            json_entry = {
                'text': entry['text'],
                'start': format_timestamp(entry).strip('[]'),
                'duration': entry['duration']
            }
            json_transcript.append(json_entry)
        return json.dumps(json_transcript, indent=2, ensure_ascii=False)
        
    elif format_type == 'srt':
        srt_lines = []
        for i, entry in enumerate(transcript, 1):
            start = format_srt_timestamp(entry['start'])
            end = format_srt_timestamp(entry['start'] + entry['duration'])
            srt_lines.extend([
                str(i),
                f"{start} --> {end}",
                entry['text'],
                ''  # Empty line between entries
            ])
        return '\n'.join(srt_lines)
        
    elif format_type == 'vtt':
        vtt_lines = ['WEBVTT\n']  # VTT header
        for i, entry in enumerate(transcript, 1):
            start = format_vtt_timestamp(entry['start'])
            end = format_vtt_timestamp(entry['start'] + entry['duration'])
            vtt_lines.extend([
                f"{start} --> {end}",
                entry['text'],
                ''  # Empty line between entries
            ])
        return '\n'.join(vtt_lines)
        
    else:
        raise ValueError(f"Invalid format type: {format_type}")

def format_timestamp(entry: dict) -> str:
    """
    Convert a transcript entry's start time (in seconds) to a formatted timestamp string.

    Args:
        entry (dict): A transcript entry dictionary containing a 'start' key
                     with the timestamp in seconds (can be float or int)

    Returns:
        str: A formatted timestamp string in the format [HH:MM:SS]

    Example:
        >>> entry = {'start': 3725.89}
        >>> format_timestamp(entry)
        '[01:02:05]'
    """
    time = int(entry['start'])
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"

def format_srt_timestamp(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format (HH:MM:SS,mmm).
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Timestamp in SRT format (HH:MM:SS,mmm)
    """
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = td.total_seconds() % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

def format_vtt_timestamp(seconds: float) -> str:
    """
    Convert seconds to VTT timestamp format (HH:MM:SS.mmm).
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Timestamp in VTT format (HH:MM:SS.mmm)
    """
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = td.total_seconds() % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

def save_to_file(content: str, filename: str, verbose: bool = False) -> None:
    """
    Save content to file and optionally display to screen.
    
    Args:
        content (str): Content to save
        filename (str): Output filename
        verbose (bool): Whether to also print content to screen
    
    Raises:
        Exception: If file cannot be written
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Transcript saved to {filename}")
        
        if verbose:
            print("\nTranscript content:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
    except Exception as e:
        print(f"Error saving file: {str(e)}", file=sys.stderr)
        sys.exit(1)

def copy_to_clipboard(content: str) -> None:
    """
    Copy content to system clipboard.
    
    Args:
        content (str): Content to copy to clipboard
        
    Raises:
        Exception: If content cannot be copied to clipboard
    """
    try:
        pyperclip.copy(content)
        print("Transcript copied to clipboard")
    except Exception as e:
        print(f"Error copying to clipboard: {str(e)}", file=sys.stderr)
        sys.exit(1)

def get_default_extension(format_type: str) -> str:
    """
    Get the default file extension for a format type.
    
    Args:
        format_type (str): Format type ('text', 'json', 'srt', or 'vtt')
        
    Returns:
        str: Default file extension including dot
    """
    extensions = {
        'text': '.txt',
        'json': '.json',
        'srt': '.srt',
        'vtt': '.vtt'
    }
    return extensions.get(format_type, '.txt')

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video transcripts')
    parser.add_argument('video_id', help='YouTube video ID or URL')
    parser.add_argument('output_file', nargs='?', help='Output file (optional)')
    parser.add_argument('--format', choices=['text', 'json', 'srt', 'vtt'],
                       default='text', help='Output format')
    parser.add_argument('--add-timestamps', action='store_true', 
                       help='Include timestamps in text format output')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Display transcript content even when saving to file')
    parser.add_argument('-c', '--clipboard', action='store_true',
                       help='Copy transcript to clipboard')
    
    args = parser.parse_args()
    
    try:
        # Extract video ID if full URL was provided
        video_id = get_video_id(args.video_id)
        
        # Get transcript
        transcript = get_transcript(video_id)
        
        # Format transcript
        formatted_transcript = format_transcript(
            transcript, 
            args.format, 
            args.add_timestamps
        )
        
        # Modify output filename if not specified
        if args.output_file and '.' not in args.output_file:
            args.output_file += get_default_extension(args.format)
        
        # Output handling
        if args.clipboard:
            copy_to_clipboard(formatted_transcript)
        
        if args.output_file:
            save_to_file(formatted_transcript, args.output_file, args.verbose)
        elif not args.clipboard:  # Only print if not copying to clipboard (unless verbose)
            print(formatted_transcript)
            
        if args.verbose and args.clipboard:
            print("\nTranscript content:")
            print("-" * 40)
            print(formatted_transcript)
            print("-" * 40)
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()