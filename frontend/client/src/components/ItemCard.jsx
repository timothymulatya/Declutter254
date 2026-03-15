import { Link } from "react-router-dom"

function ItemCard({ item }) {

  const cardStyle = {
    background: "white",
    borderRadius: "16px",
    overflow: "hidden",
    boxShadow: "0 4px 15px rgba(0,0,0,0.08)",
    transition: "transform 0.3s ease",
    display: "flex",
    flexDirection: "column",
    height: "100%"
  }

  const imageStyle = {
    width: "100%",
    height: "140px",
    objectFit: "cover",
    background: "#f0f0f0"
  }

  const contentStyle = {
    padding: "12px",
    display: "flex",
    flexDirection: "column",
    flex: 1
  }

  return (
    <div style={cardStyle} className="item-card">
      <img src={item.photo_url || "https://via.placeholder.com/300x200?text=No+Photo"} alt={item.title} style={imageStyle} />

      <div style={contentStyle}>
        <h3 style={{ fontSize: "1rem", margin: "0 0 8px 0", color: "var(--neutral-black)" }}>{item.title}</h3>

        <div style={{ fontSize: "0.8rem", color: "#666", marginBottom: "12px" }}>
          <div style={{ marginBottom: "4px" }}>Location: {item.pickup_location}</div>
          <div style={{
            display: "inline-block",
            padding: "2px 8px",
            borderRadius: "4px",
            background: "rgba(0, 191, 255, 0.1)",
            color: "var(--primary-skyblue)",
            fontWeight: "bold"
          }}>
            {item.category_name}
          </div>
        </div>

        <Link
          to={`/item/${item.id}`}
          style={{
            textDecoration: "none",
            marginTop: "auto",
            display: "block",
            textAlign: "center",
            padding: "8px",
            background: "var(--accent-maroon)",
            color: "white",
            borderRadius: "8px",
            fontSize: "0.9rem",
            fontWeight: "600"
          }}
        >
          View Details
        </Link>
      </div>
    </div>
  )
}

export default ItemCard