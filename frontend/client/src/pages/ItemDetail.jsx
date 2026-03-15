import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchItem } from "../api/api";
import RequestForm from "../components/RequestForm";

function ItemDetail() {
  const { id } = useParams();
  const [item, setItem] = useState(null);

  useEffect(() => {
    fetchItem(id).then(data => {
      setItem(data);
    });
  }, [id]);

  if (!item) return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h2 style={{ color: "var(--primary-skyblue)" }}>Loading...</h2>
    </div>
  );

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <div style={{
        background: "white",
        borderRadius: "20px",
        overflow: "hidden",
        boxShadow: "0 10px 30px rgba(0,0,0,0.05)"
      }}>
        <img
          src={item.photo_url || "https://via.placeholder.com/600x400?text=Item+Photo"}
          alt={item.title}
          style={{ width: "100%", height: "300px", objectFit: "cover" }}
        />

        <div style={{ padding: "24px" }}>
          <h2 style={{ fontSize: "2rem", color: "var(--neutral-black)", marginBottom: "16px" }}>{item.title}</h2>

          <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "24px" }}>
            <span style={{
              background: "rgba(0, 191, 255, 0.1)",
              color: "var(--primary-skyblue)",
              padding: "4px 12px",
              borderRadius: "20px",
              fontSize: "0.9rem",
              fontWeight: "600"
            }}>
              {item.category_name}
            </span>
            <span style={{
              background: "#f0f0f0",
              color: "#666",
              padding: "4px 12px",
              borderRadius: "20px",
              fontSize: "0.9rem"
            }}>
              {item.condition}
            </span>
          </div>

          <p style={{ fontSize: "1.1rem", color: "#444", marginBottom: "32px", lineHeight: "1.8" }}>
            {item.description}
          </p>

          <div style={{
            background: "var(--bg-light)",
            padding: "20px",
            borderRadius: "12px",
            marginBottom: "32px"
          }}>
            <h3 style={{ fontSize: "1.1rem", marginBottom: "12px" }}>Pickup Details</h3>
            <div style={{ color: "#555", fontSize: "0.95rem" }}>
              <p><strong>Location:</strong> {item.pickup_location}</p>
              {item.pickup_days && <p>📅 <strong>Days:</strong> {item.pickup_days}</p>}
              {item.pickup_times && <p>🕒 <strong>Times:</strong> {item.pickup_times}</p>}
            </div>
          </div>

          <div style={{ borderTop: "1px solid #eee", paddingTop: "32px" }}>
            <h3 style={{ marginBottom: "20px", color: "var(--accent-maroon)" }}>Interested in this item?</h3>
            <RequestForm itemId={item.id} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ItemDetail;