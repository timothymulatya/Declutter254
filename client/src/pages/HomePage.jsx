import { useEffect, useState } from "react"
import { fetchItems } from "../api/items"
import FilterBar from "../components/FilterBar"
import SearchBar from "../components/SearchBar"

function HomePage(){

  const [items, setItems] = useState([])
  const [filteredItems, setFilteredItems] = useState([])

  useEffect(() => {

    fetchItems().then(data => {
      setItems(data)
      setFilteredItems(data)
    })

  }, [])


  function handleFilter(filters){

    let result = items

    if(filters.category){
      result = result.filter(item => item.category === filters.category)
    }

    if(filters.location){
      result = result.filter(item =>
        item.location.toLowerCase().includes(filters.location.toLowerCase())
      )
    }

    setFilteredItems(result)

  }


  function handleSearch(query){

    if(!query){
      setFilteredItems(items)
      return
    }

    const result = items.filter(item =>
      item.title.toLowerCase().includes(query.toLowerCase())
    )

    setFilteredItems(result)

  }


  return(

    <div>

      <h1>Available Items</h1>

      <SearchBar onSearch={handleSearch} />

      <FilterBar onFilter={handleFilter} />

      <div>

        {filteredItems.map(item => (

          <div
            key={item.id}
            style={{
              border:"1px solid #ccc",
              padding:"10px",
              margin:"10px"
            }}
          >

            <h3>{item.title}</h3>

            <p>{item.description}</p>

            <p><strong>Category:</strong> {item.category}</p>

            <p><strong>Location:</strong> {item.location}</p>

          </div>

        ))}

      </div>

    </div>

  )

}

export default HomePage 