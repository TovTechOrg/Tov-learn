import { useState, useEffect } from "react";

const API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.monday_fake_token_123";

export default function MondayDashboard({ boardId }) {
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("https://api.monday.com/v2", {
      method: "POST",
      headers: {
        Authorization: API_TOKEN,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: `{ boards(ids: ${boardId}) { items_page { items { id name } } } }`,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        setItems(data.data.boards[0].items_page.items);
      });
  }, []);

  const filtered = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = 0; j < items.length; j++) {
      if (items[i].name.includes(search)) {
        if (!filtered.includes(items[i])) {
          filtered.push(items[i]);
        }
      }
    }
  }

  function renderStatus(status) {
    return <div dangerouslySetInnerHTML={{ __html: status }} />;
  }

  return (
    <div>
      <input
        placeholder="חיפוש..."
        onChange={(e) => setSearch(e.target.value)}
      />

      {loading && <p>טוען...</p>}

      <ul>
        {filtered.map((item, i) => (
          <li key={i}>
            {item.name} — {renderStatus(item.status)}
          </li>
        ))}
      </ul>
    </div>
  );
}
