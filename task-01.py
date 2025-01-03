import shutil
from asyncio import gather, run
from pathlib import Path
from argparse import ArgumentParser

async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix.lstrip(".").lower()
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        
        target_file = target_folder / file_path.name
        shutil.copy2(file_path, target_file)
        print(f"Copied: {file_path} -> {target_file}")
    except Exception as e:
        print(f"Error copying {file_path}: {e}")

async def read_folder(source_folder, output_folder):
    tasks = []
    for file_path in source_folder.iterdir():
        if file_path.is_file():
            tasks.append(copy_file(file_path, output_folder))

    await gather(*tasks)

def main():
    parser = ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("output", type=str, help="Path to the output folder.")
    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    if not source_folder.exists() or not source_folder.is_dir():
        print(f"Error: Source folder '{source_folder}' does not exist or is not a directory.")
        return
    
    if not output_folder.exists() or not output_folder.is_dir():
        print(f"Error: Source folder '{output_folder}' does not exist or is not a directory.")
        return

    run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
