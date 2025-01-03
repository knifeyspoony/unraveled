import httpx

from unraveled.test import _REPO_ROOT


def test_socket_challenge():
    socket_challenges_dir = (
        _REPO_ROOT / "samples" / "247ctf" / "beginner_tutorial" / "socket_challenges"
    )
    assert socket_challenges_dir.exists(), "Socket challenges directory is required."

    instructions_file = socket_challenges_dir / "instructions.txt"
    flag_file = socket_challenges_dir / "flag.txt"

    assert (
        instructions_file.exists() and flag_file.exists()
    ), "Instructions and flag files are required."

    instructions = instructions_file.read_text()
    flag = flag_file.read_text()

    response = httpx.post(
        "http://localhost:8001/RunWorkflow",
        json={"message": instructions},
    )
    assert response.status_code == 200
