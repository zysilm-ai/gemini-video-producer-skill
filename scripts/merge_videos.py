#!/usr/bin/env python3
"""
Video Merging Script for AI Video Producer

Merges N video files into a single output video using moviepy.

Usage:
    python merge_videos.py -o output.mp4 video1.mp4 video2.mp4 video3.mp4 ...
    python merge_videos.py --output output.mp4 --inputs video1.mp4 video2.mp4

Arguments:
    -o, --output    Output video file path (required)
    -i, --inputs    Input video files to merge (alternative to positional args)
    --method        Concatenation method: 'compose' or 'chain' (default: compose)
    --codec         Video codec (default: libx264)
    --fps           Output FPS (default: use first video's FPS)
    --resize        Resize to match first video's resolution (default: True)

Examples:
    # Merge scene segments
    python merge_videos.py -o scene-01/scene.mp4 scene-01/seg-A.mp4 scene-01/seg-B.mp4

    # Merge all scenes into final video
    python merge_videos.py -o output.mp4 scene-01/scene.mp4 scene-02/scene.mp4 scene-03/scene.mp4
"""

import argparse
import sys
import os
from pathlib import Path


def merge_videos(input_files: list, output_file: str, method: str = 'compose',
                 codec: str = 'libx264', fps: int = None, resize: bool = True) -> dict:
    """
    Merge multiple video files into a single output video.

    Args:
        input_files: List of input video file paths
        output_file: Output video file path
        method: Concatenation method ('compose' or 'chain')
        codec: Video codec for output
        fps: Output FPS (None = use first video's FPS)
        resize: Whether to resize all videos to match first video's resolution

    Returns:
        dict with status, output_path, duration, and message
    """
    try:
        from moviepy import VideoFileClip, concatenate_videoclips
    except ImportError:
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
        except ImportError:
            return {
                "status": "error",
                "message": "moviepy not installed. Run: pip install moviepy"
            }

    # Validate inputs
    if len(input_files) < 2:
        return {
            "status": "error",
            "message": f"Need at least 2 input files, got {len(input_files)}"
        }

    # Check all input files exist
    missing = [f for f in input_files if not os.path.exists(f)]
    if missing:
        return {
            "status": "error",
            "message": f"Missing input files: {missing}"
        }

    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    clips = []
    target_size = None
    target_fps = fps

    try:
        # Load all clips
        print(f"Loading {len(input_files)} video files...")
        for i, input_file in enumerate(input_files):
            print(f"  [{i+1}/{len(input_files)}] Loading: {input_file}")
            clip = VideoFileClip(input_file)

            # Get target size and fps from first clip
            if i == 0:
                target_size = clip.size
                if target_fps is None:
                    target_fps = clip.fps
                print(f"  Target resolution: {target_size[0]}x{target_size[1]}, FPS: {target_fps}")

            # Resize if needed
            if resize and clip.size != target_size:
                print(f"  Resizing from {clip.size} to {target_size}")
                clip = clip.resized(target_size)

            clips.append(clip)

        # Concatenate clips
        print(f"Concatenating {len(clips)} clips using method: {method}...")
        if method == 'compose':
            final = concatenate_videoclips(clips, method='compose')
        else:
            final = concatenate_videoclips(clips)

        # Write output
        print(f"Writing output to: {output_file}")
        print(f"  Codec: {codec}, FPS: {target_fps}")

        final.write_videofile(
            output_file,
            codec=codec,
            fps=target_fps,
            audio=False,
            logger='bar'
        )

        duration = final.duration

        # Cleanup
        print("Cleaning up...")
        final.close()
        for clip in clips:
            clip.close()

        result = {
            "status": "success",
            "output_path": output_file,
            "duration": duration,
            "resolution": f"{target_size[0]}x{target_size[1]}",
            "fps": target_fps,
            "input_count": len(input_files),
            "message": f"Successfully merged {len(input_files)} videos into {output_file} ({duration:.1f}s)"
        }
        print(f"\n{result['message']}")
        return result

    except Exception as e:
        # Cleanup on error
        for clip in clips:
            try:
                clip.close()
            except:
                pass
        return {
            "status": "error",
            "message": f"Error merging videos: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(
        description='Merge multiple video files into a single output video',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -o scene.mp4 seg-A.mp4 seg-B.mp4 seg-C.mp4
  %(prog)s --output final.mp4 scene-01.mp4 scene-02.mp4 scene-03.mp4
  %(prog)s -o output.mp4 --codec libx264 --fps 24 video1.mp4 video2.mp4
        """
    )

    parser.add_argument(
        'inputs',
        nargs='*',
        help='Input video files to merge (in order)'
    )

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output video file path'
    )

    parser.add_argument(
        '-i', '--input-files',
        nargs='+',
        dest='input_files',
        help='Input video files (alternative to positional arguments)'
    )

    parser.add_argument(
        '--method',
        choices=['compose', 'chain'],
        default='compose',
        help='Concatenation method (default: compose)'
    )

    parser.add_argument(
        '--codec',
        default='libx264',
        help='Video codec (default: libx264)'
    )

    parser.add_argument(
        '--fps',
        type=int,
        default=None,
        help='Output FPS (default: use first video\'s FPS)'
    )

    parser.add_argument(
        '--no-resize',
        action='store_true',
        help='Do not resize videos to match first video\'s resolution'
    )

    args = parser.parse_args()

    # Get input files from either positional args or -i flag
    input_files = args.inputs if args.inputs else []
    if args.input_files:
        input_files.extend(args.input_files)

    if len(input_files) < 2:
        parser.error("Need at least 2 input video files")

    # Run merge
    result = merge_videos(
        input_files=input_files,
        output_file=args.output,
        method=args.method,
        codec=args.codec,
        fps=args.fps,
        resize=not args.no_resize
    )

    # Exit with appropriate code
    if result['status'] == 'success':
        sys.exit(0)
    else:
        print(f"ERROR: {result['message']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
