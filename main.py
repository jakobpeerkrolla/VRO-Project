"""Run the safe import and preprocessing step from the project root."""

from src.data_preprocessing import preprocess_file
from src.utils import ensure_directories, get_logger, load_config


def main() -> None:
    """Load configuration and create the processed dataset."""
    config = load_config()
    ensure_directories(config)
    report = preprocess_file(config["data"]["raw_path"], config["data"]["processed_path"])
    get_logger().info("Preprocessing complete: %s", report)


if __name__ == "__main__":
    main()
