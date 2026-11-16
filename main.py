from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import random

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


def generate_maze(rows=17, cols=25):
    maze = [
        [
            {
                "top": True,
                "right": True,
                "bottom": True,
                "left": True
            }
            for _ in range(cols)
        ]
        for _ in range(rows)
    ]

    visited = [[False] * cols for _ in range(rows)]

    directions = [
        (-1, 0, "top", "bottom"),
        (0, 1, "right", "left"),
        (1, 0, "bottom", "top"),
        (0, -1, "left", "right")
    ]

    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        row, col = stack[-1]

        neighbors = []

        for dr, dc, wall, opposite in directions:
            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and not visited[nr][nc]
            ):
                neighbors.append((nr, nc, wall, opposite))

        if neighbors:
            nr, nc, wall, opposite = random.choice(neighbors)

            maze[row][col][wall] = False
            maze[nr][nc][opposite] = False

            visited[nr][nc] = True
            stack.append((nr, nc))

        else:
            stack.pop()

    # Вход и выход
    maze[0][0]["left"] = False
    maze[rows - 1][cols - 1]["right"] = False

    return maze


@app.get("/", response_class=HTMLResponse)
async def index():
    html = (BASE_DIR / "static" / "index.html").read_text(
        encoding="utf-8"
    )
    return HTMLResponse(html)


@app.get("/api/maze")
async def get_maze():
    return {
        "maze": generate_maze(),
        "rows": 17,
        "cols": 25
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
