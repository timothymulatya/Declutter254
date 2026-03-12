import { useState } from "react";

function FilterBar({items, setFilteredItems}) {

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  function handleSearch(value) {

    setSearch(value);

    const filtered = items.filter(item =>
      item.title.toLowerCase().includes(value.toLowerCase())
    );

    setFilteredItems(filtered);
  }

  function handleCategory(value) {

    setCategory(value);

    const filtered = items.filter(item =>
      item.category === value || value === ""
    );

    setFilteredItems(filtered);
  }

  return (

    <div style={{margin:"20px 0"}}>

      <input
        type="text"
        placeholder="Search items..."
        value={search}
        onChange={(e)=>handleSearch(e.target.value)}
      />

      <select
        value={category}
        onChange={(e)=>handleCategory(e.target.value)}
      >

        <option value="">All Categories</option>
        <option value="Kitchen">Kitchen</option>
        <option value="Furniture">Furniture</option>
        <option value="Clothes">Clothes</option>
        <option value="Books">Books</option>
        <option value="Electronics">Electronics</option>

      </select>

    </div>

  );
}

export default FilterBar; 