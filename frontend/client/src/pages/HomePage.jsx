import { useEffect, useState } from "react"
import { fetchItems } from "../api/api"
import FilterBar from "../components/FilterBar"
import SearchBar from "../components/SearchBar"
import ItemCard from "../components/ItemCard"

function HomePage() {

  const [items, setItems] = useState([])
  const [filteredItems, setFilteredItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {

    fetchItems().then(data => {
      const itemsList = data.items || data;
      setItems(itemsList)
      setFilteredItems(itemsList)
      setLoading(false)
    })

  }, [])


  function handleFilter(filters) {

    let result = items

    if (filters.category) {
      result = result.filter(item => item.category === filters.category)
    }

    if (filters.location) {
      result = result.filter(item =>
        item.location.toLowerCase().includes(filters.location.toLowerCase())
      )
    }

    setFilteredItems(result)

  }


  function handleSearch(query) {

    if (!query) {
      setFilteredItems(items)
      return
    }

    const result = items.filter(item =>
      item.title.toLowerCase().includes(query.toLowerCase())
    )

    setFilteredItems(result)

  }


  if (loading) {

    return (

      <div style={{ padding: "30px", textAlign: "center" }}>

        <h2>Loading items...</h2>

      </div>

    )

  }


  return (

    <div style={{ padding: "20px", maxWidth: "1200px", margin: "0 auto" }}>

      <h1 style={{ fontSize: "1.8rem", marginBottom: "8px", color: "var(--accent-maroon)" }}>Available Items</h1>
      <p style={{ color: "#666", marginBottom: "24px" }}>Find what you need, give what you don't.</p>

      <div style={{ marginBottom: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>
        <SearchBar onSearch={handleSearch} />
        <FilterBar onFilter={handleFilter} />
      </div>

      {filteredItems.length === 0 ? (

        <div
          style={{
            marginTop: "60px",
            textAlign: "center",
            color: "#666",
            padding: "40px",
            background: "white",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.05)"
          }}
        >

          <h2 style={{ color: "var(--accent-maroon)" }}>No items found</h2>
          <p>Try adjusting your search or filters.</p>

        </div>

      ) : (

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))",
            gap: "16px",
            marginTop: "30px"
          }}
        >

          {filteredItems.map(item => (

            <ItemCard key={item.id} item={item} />

          ))}

        </div>

      )}

    </div>

  )

}

export default HomePage 