# YouTube Transcript Downloader

yt-transcript-dl.py is a Python script that downloads the transcript of a YouTube video and optionally includes timestamps. The transcript can be printed to the console, saved to a file, or copied to the clipboard.

## Requirements

- Python 3.x
- [`youtube_transcript_api`](https://pypi.org/project/youtube-transcript-api/)
- [`pyperclip`](https://pypi.org/project/pyperclip/)

You can install the required libraries using pip:

```sh
pip install youtube-transcript-api pyperclip
```

## Usage

```sh
python yt-transcript-dl.py <video_id_or_url> [output_file] [--format FORMAT] [--add-timestamps] [-v] [-c]
```

- `<video_id_or_url>`: The YouTube video ID or URL.
- `[output_file]`: (Optional) The file to save the transcript. If not provided, the transcript will be printed to the console.
- `[--format FORMAT]`: (Optional) The output format. Choices are `text`, `json`, `srt`, and `vtt`. Defaults to `text`.
- `[--add-timestamps]`: (Optional) Include this flag to add timestamps to the transcript in text format.
- `[-v]`: (Optional) Verbose mode. Display transcript content even when saving to file.
- `[-c]`: (Optional) Copies the transcript output to the clipboard.

### Examples

1. Print the transcript of a YouTube video to the console:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ
    ```

2. Save the transcript to a file:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ transcript.txt
    ```

3. Print the transcript with timestamps:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ --add-timestamps
    ```

4. Save the transcript with timestamps to a file:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ transcript.txt --add-timestamps
    ```

5. Copy the transcript to the clipboard:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ -c
    ```

6. Save the transcript in JSON format:

    ```sh
    python yt-transcript-dl.py dQw4w9WgXcQ transcript.json --format json
    ```

## Contribute

We welcome contributions! Follow these steps to contribute:

1. **Fork the repository**: Click the "Fork" button at the top right of this page to create a copy of this repository in your GitHub account.

2. **Clone the repository**: Clone your forked repository to your local machine using the following command:
    ```sh
    git clone https://github.com/your-username/yt-transcript-dl.git
    ```

3. **Create a new branch**: Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b my-feature-branch
    ```

4. **Make your changes**: Make your changes to the codebase.

5. **Commit your changes**: Commit your changes with a descriptive commit message:
    ```sh
    git commit -am 'Add new feature'
    ```

6. **Push to the branch**: Push your changes to your forked repository:
    ```sh
    git push origin my-feature-branch
    ```

7. **Create a Pull Request**: Go to the original repository on GitHub and create a pull request from your forked repository. Provide a clear description of your changes.

We will review your pull request and provide feedback. Once approved, your changes will be merged into the main branch.

Thank you for your contribution!

## License

This project is licensed under the MIT License. See the LICENSE file for details.