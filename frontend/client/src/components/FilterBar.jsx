import { useState } from "react";

function FilterBar({ onFilter }) {
  const [category, setCategory] = useState("");

  function handleCategory(value) {
    setCategory(value);
    onFilter({ category: value });
  }

  return (
    <div style={{ margin: "0 0 20px 0", width: "100%" }}>
      <select
        value={category}
        onChange={(e) => handleCategory(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "12px",
          border: "2px solid #eee",
          background: "white",
          fontSize: "1rem",
          fontWeight: "500",
          color: "var(--neutral-black)",
          cursor: "pointer"
        }}
      >
        <option value="">All Categories</option>
        <option value="Electronics">Electronics</option>
        <option value="Furniture">Furniture</option>
        <option value="Clothing">Clothing</option>
        <option value="Books">Books</option>
        <option value="Home Appliances">Home Appliances</option>
      </select>
    </div>
  );
}

export default FilterBar;