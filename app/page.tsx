'use client'

import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState<string>("")

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/python');
        const data = await response.json();
        setMessage(data.message);
      }catch (error) {
        console.log('error', error);
    }};
    fetchData();
  },[]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Home Page</h1>
      <p>{message || 'Loading...'}</p>
    </main>
  );
}
