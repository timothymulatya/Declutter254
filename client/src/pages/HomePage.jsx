import { useEffect, useState } from "react";
import { fetchItems } from "../api/api";
import { Link } from "react-router-dom";
import FilterBar from "../components/FilterBar";

function HomePage() {

  const [items, setItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);

  useEffect(() => {
    fetchItems().then(data => {
      setItems(data);
      setFilteredItems(data);
    });
  }, []);

  return (
    <div>

      <h1>Available Items</h1>

      <FilterBar items={items} setFilteredItems={setFilteredItems} />

      {filteredItems.map(item => (

        <div key={item.id} style={{border:"1px solid gray", margin:"10px", padding:"10px"}}>

          <h3>{item.title}</h3>

          <p>{item.description}</p>

          <Link to={`/item/${item.id}`}>
            View Details
          </Link>

        </div>

      ))}

    </div>
  );
}

export default HomePage; 