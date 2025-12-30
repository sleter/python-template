"""Integration tests for Dockerfile."""

import subprocess
from pathlib import Path

import pytest


def test_dockerfile_builds_and_runs_successfully() -> None:
    """Test that the Dockerfile builds successfully and the container starts and runs correctly."""
    project_root = Path(__file__).parent.parent.parent
    image_name = "project-test:latest"
    container_name = "project-test-container"

    # Check if Docker is available
    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("Docker is not available")

    try:
        # Build the Docker image
        build_result = subprocess.run(
            ["docker", "build", "-t", image_name, "."],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert build_result.returncode == 0, f"Docker build failed: {build_result.stderr}"

        # Run the container and capture output
        run_result = subprocess.run(
            ["docker", "run", "--name", container_name, "--rm", image_name],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Verify the container ran successfully
        assert run_result.returncode == 0, f"Container failed to run: {run_result.stderr}"

        # Verify the expected output
        assert "Hello, World!" in run_result.stdout, f"Expected output not found. Got: {run_result.stdout}"

    finally:
        # Cleanup: Remove the container if it exists (in case it wasn't removed)
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            check=False,
            capture_output=True,
            timeout=10,
        )

        # Cleanup: Remove the image
        subprocess.run(
            ["docker", "rmi", "-f", image_name],
            check=False,
            capture_output=True,
            timeout=30,
        )


def test_dockerfile_uses_correct_environment_variables() -> None:
    """Test that the Dockerfile sets the correct environment variables."""
    project_root = Path(__file__).parent.parent.parent
    image_name = "project-test-env:latest"
    container_name = "project-test-env-container"

    # Check if Docker is available
    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pytest.skip("Docker is not available")

    try:
        # Build the Docker image
        subprocess.run(
            ["docker", "build", "-t", image_name, "."],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )

        # Run container and check environment variable
        env_check_result = subprocess.run(
            [
                "docker",
                "run",
                "--name",
                container_name,
                "--rm",
                image_name,
                "sh",
                "-c",
                "echo $LOGURU_LEVEL",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert env_check_result.returncode == 0, f"Failed to check environment: {env_check_result.stderr}"
        assert "INFO" in env_check_result.stdout, f"LOGURU_LEVEL not set correctly. Got: {env_check_result.stdout}"

    finally:
        # Cleanup: Remove the container if it exists
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            check=False,
            capture_output=True,
            timeout=10,
        )

        # Cleanup: Remove the image
        subprocess.run(
            ["docker", "rmi", "-f", image_name],
            check=False,
            capture_output=True,
            timeout=30,
        )
