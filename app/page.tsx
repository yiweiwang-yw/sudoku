'use client'

import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/python');
        const data = await response.json();
        setMessage(data.message);
      } catch (error) {
        console.log('error', error);
      }
    };
    fetchData();
  }, []);

  // Function to render the Sudoku board cells
  const renderSudokuBoard = () => {
    const rows = new Array(9).fill(null);
    const cols = new Array(9).fill(null);

    return rows.map((_, rowIndex) => (
      <div key={`row-${rowIndex}`} className="flex">
        {cols.map((_, colIndex) => (
          <div
            key={`cell-${rowIndex}-${colIndex}`}
            className={`w-10 h-10 border-b border-r ${rowIndex % 3 === 2 && colIndex % 3 === 2 ? 'border-b-2 border-r-2' : ''} ${rowIndex === 8 ? 'border-b-2' : ''} ${colIndex === 8 ? 'border-r-2' : ''}`}
            style={{
              borderTop: rowIndex === 0 ? '2px solid' : 'none',
              borderLeft: colIndex === 0 ? '2px solid' : 'none',
              borderBottom: rowIndex % 3 === 2 ? '2px solid' : '1px dashed',
              borderRight: colIndex % 3 === 2 ? '2px solid' : '1px dashed',
            }}
          >
            {}
          </div>
        ))}
      </div>
    ));
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-2xl font-bold mb-6">Home Page</h1>
      <p className="mb-6">{message || 'Loading...'}</p>
      <div>
        {renderSudokuBoard()}
      </div>
    </main>
  );
}
