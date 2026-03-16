import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";

const schema = Yup.object({
  name: Yup.string().required("Name required"),
  phone: Yup.string()
    .matches(/^(07|01)\d{8}$/, "Invalid Kenyan phone number")
    .required("Phone required"),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password required"),
  estate: Yup.string().required("Estate required"),
  landmark: Yup.string().required("Landmark required")
});

function Signup() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  async function handleSubmit(values, { setSubmitting }) {
    setError("");
    const userData = {
      name: values.name,
      phone_number: values.phone,
      password: values.password,
      location: `${values.estate}, ${values.landmark}`
    };

    const result = await register(userData);
    if (result.success) {
      navigate("/");
    } else {
      setError(result.error);
    }
    setSubmitting(false);
  }

  return (
    <div style={{ padding: "40px 20px", maxWidth: "450px", margin: "0 auto" }}>
      <div style={{ background: "white", padding: "32px", borderRadius: "20px", boxShadow: "0 10px 40px rgba(0,0,0,0.05)" }}>
        <h2 style={{ fontSize: "1.8rem", marginBottom: "8px", color: "var(--accent-maroon)" }}>Join Declutter254</h2>
        <p style={{ color: "#666", marginBottom: "32px" }}>Start giving and receiving today.</p>

        {error && (
          <div style={{
            background: "#fff5f5",
            color: "var(--accent-maroon)",
            padding: "12px",
            borderRadius: "8px",
            marginBottom: "20px",
            fontSize: "0.9rem",
            border: "1px solid #fed7d7"
          }}>
            {error}
          </div>
        )}

        <Formik
          initialValues={{
            name: "",
            phone: "",
            password: "",
            estate: "",
            landmark: ""
          }}
          validationSchema={schema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", marginBottom: "6px", fontWeight: "600", fontSize: "0.85rem" }}>Full Name</label>
                <Field name="name" placeholder="Enter your name" className="form-input" />
                <ErrorMessage name="name" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
              </div>

              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", marginBottom: "6px", fontWeight: "600", fontSize: "0.85rem" }}>Phone Number</label>
                <Field name="phone" placeholder="e.g. 0712345678" className="form-input" />
                <ErrorMessage name="phone" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
              </div>

              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", marginBottom: "6px", fontWeight: "600", fontSize: "0.85rem" }}>Password</label>
                <Field type="password" name="password" placeholder="Min 6 characters" className="form-input" />
                <ErrorMessage name="password" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
              </div>

              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", marginBottom: "6px", fontWeight: "600", fontSize: "0.85rem" }}>Estate / Area</label>
                <Field name="estate" placeholder="e.g. Westlands" className="form-input" />
                <ErrorMessage name="estate" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
              </div>

              <div style={{ marginBottom: "16px" }}>
                <label style={{ display: "block", marginBottom: "6px", fontWeight: "600", fontSize: "0.85rem" }}>Landmark</label>
                <Field name="landmark" placeholder="e.g. Next to Total Station" className="form-input" />
                <ErrorMessage name="landmark" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
              </div>

              <button
                type="submit"
                className="btn-primary"
                style={{ width: "100%", marginTop: "10px", padding: "14px" }}
                disabled={isSubmitting}
              >
                {isSubmitting ? "Creating Account..." : "Create Account"}
              </button>
            </Form>
          )}
        </Formik>

        <p style={{ marginTop: "24px", textAlign: "center", fontSize: "0.9rem", color: "#666" }}>
          Already have an account? <Link to="/login" style={{ color: "var(--primary-skyblue)", fontWeight: "600", textDecoration: "none" }}>Log in</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
