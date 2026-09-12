# Sudoku

A Sudoku board and solver built with Next.js 13 and FastAPI. You can edit an
empty board, solve a complete puzzle, or reveal one solution step at a time.

## Prerequisites

- Node.js 18 or newer
- Python 3.9 or newer
- `pip`

## Local setup

Install the JavaScript and Python dependencies:

```bash
npm install
python -m pip install -r requirements.txt
```

Start Next.js and FastAPI together:

```bash
npm run dev
```

Open <http://localhost:3000>. FastAPI runs on <http://127.0.0.1:8000>, and
Next.js proxies `/api` requests to it in development.

The board starts with a bundled puzzle and does not require AWS. **Solve** and
**Solve Next** submit the current board to FastAPI. Inputs must be a 9-by-9
board containing `.` for empty cells or digits `1` through `9`. Conflicting and
unsatisfiable puzzles are reported without changing the board.

## Configuration

The Random and difficulty controls use the existing DynamoDB integration. They
expect a table with the schema created by `dynamo.py`:

- table name: `SudokuPuzzles` by default
- partition key: `puzzle_id`
- global secondary index: `difficulty-index`
- index partition key: `difficulty`
- index sort key: `puzzle_id`

Configure AWS credentials and region through boto3's standard environment
variables, shared AWS profile, or workload role. Set `SUDOKU_TABLE_NAME` to use
a different table. When credentials, region, or the table are unavailable,
puzzle-loading endpoints return HTTP 503; the bundled puzzle and solver remain
usable.

The frontend uses same-origin `/api` requests by default. When the API is hosted
separately, set `NEXT_PUBLIC_API_BASE_URL` to its API prefix, for example:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
```

Do not place AWS credentials in this variable or commit them to the repository.

## Validation

Run the focused Python tests:

```bash
python -m unittest discover -s api/tests
```

Run frontend checks and the production build:

```bash
npx tsc --noEmit
npm run lint
npm run build
```

## Deployment

The existing deployment is available at <https://yw-sudoku.vercel.app/>.
