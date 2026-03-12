import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{padding:"10px", background:"#eee"}}>
      <Link to="/">Home</Link> |{" "}
      <Link to="/post-item">Post Item</Link> |{" "}
      <Link to="/profile">Profile</Link> |{" "}
      <Link to="/requests">Requests</Link> |{" "}
      <Link to="/login">Login</Link>
    </nav>
  );
}

export default Navbar; 