"use client";

import { useEffect, useState } from "react";
import {
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownItem,
    Button,
} from "@nextui-org/react";
const { DynamoDBClient, ListTablesCommand } = require("@aws-sdk/client-dynamodb");

interface SudokuData {
    id: number;
    puzzle: string[][];
    solution: string[][];
    clues: number;
    difficulty: string;
}

// const apiBaseUrl = "http://127.0.0.1:8000/api";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

const client = new DynamoDBClient({
    region : process.env.NEXT_PUBLIC_AWS_REGION,
    credentials: {
        accessKeyId: process.env.NEXT_PUBLIC_AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.NEXT_PUBLIC_AWS_SECRET_ACCESS_KEY,
    },
});


async function listTables() {
    try {
        const data = await client.send(new ListTablesCommand({}));
        console.log("Tables:", data.TableNames.join("\n"));
    } catch (err) {
        console.error(err);
    }
}

listTables();

export default function Home() {
    const [message, setMessage] = useState<string>("");
    const [puzzleData, setPuzzleData] = useState<SudokuData | null>(null);

    async function fetchRandomSudoku() {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/get_randomsudoku`
            );
            const data: SudokuData = await response.json();
            setMessage("Puzzle loaded");
            setPuzzleData(data);
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    async function fetchSudokuByDifficulty(difficulty: any) {
        try {
            const response = await fetch(
                `${apiBaseUrl}/python/sudoku/difficulty/${difficulty}`
            );
            const data: SudokuData = await response.json();
            setMessage(`Puzzle loaded with difficulty: ${difficulty}`);
            setPuzzleData(data);
        } catch (error) {
            console.error("error", error);
            setMessage("Failed to load puzzle");
        }
    }

    useEffect(() => {
        setPuzzleData(initializeEmptyBoard());
    }, []);

    const initializeEmptyBoard = () => {
        const emptyBoard = Array.from({ length: 9 }, () => Array(9).fill("."));
        setMessage("Board initialized");
        return {
            id: 0,
            puzzle: emptyBoard,
            solution: emptyBoard,
            clues: 0,
            difficulty: "none",
        };
    };

    const clearSudokuBoard = () => {
        setPuzzleData(initializeEmptyBoard());
        setMessage("Board cleared");
    };

    const renderSudokuBoard = () => {
        if (!puzzleData) {
            return <div>Loading...</div>;
        }

        return puzzleData.puzzle.map((row: string[], rowIndex: number) => (
            <div key={`row-${rowIndex}`} className="flex">
                {row.map((value: string, colIndex: number) => (
                    <div
                        key={`cell-${rowIndex}-${colIndex}`}
                        className={`w-10 h-10 flex items-center justify-center border ${
                            rowIndex % 3 === 2 && colIndex % 3 === 2
                                ? "border-b-2 border-r-2"
                                : ""
                        } ${rowIndex === 8 ? "border-b-2" : ""} ${
                            colIndex === 8 ? "border-r-2" : ""
                        }`}
                        style={{
                            borderTop: rowIndex === 0 ? "2px solid" : "none",
                            borderLeft: colIndex === 0 ? "2px solid" : "none",
                            borderBottom:
                                rowIndex % 3 === 2 ? "2px solid" : "1px solid",
                            borderRight:
                                colIndex % 3 === 2 ? "2px solid" : "1px solid",
                            fontSize: "16px",
                            fontFamily: "monospace",
                        }}
                    >
                        {value !== "." ? value : ""}
                    </div>
                ))}
            </div>
        ));
    };

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <h1 className="text-2xl font-bold mb-6">Home Page</h1>
            <p className="mb-6">{message || "Loading..."}</p>
            <div className="mb-6">
                <Button color="primary" onClick={fetchRandomSudoku}>
                    Random
                </Button>
                <Button color="primary" onClick={clearSudokuBoard}>
                    Clear
                </Button>
                <Dropdown>
                    <DropdownTrigger>
                        <Button variant="bordered" color="primary">
                            Select Difficulty
                        </Button>
                    </DropdownTrigger>
                    <DropdownMenu aria-label="Static Actions" onAction={(key) => fetchSudokuByDifficulty(String(key))}>
                        <DropdownItem key="low">Simple</DropdownItem>
                        <DropdownItem key="medium">Medium</DropdownItem>
                        <DropdownItem key="high">Hard</DropdownItem>
                    </DropdownMenu>
                </Dropdown>
            </div>
            <div>{renderSudokuBoard()}</div>
        </main>
    );
}
