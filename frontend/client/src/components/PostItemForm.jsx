import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { createItem } from "../api/api";
import { useNavigate } from "react-router-dom";
import {
  Package,
  AlignLeft,
  MapPin,
  Calendar,
  Clock,
  Image as ImageIcon,
  Info,
  Tag
} from "lucide-react";

const schema = Yup.object({
  title: Yup.string().required("Title required"),
  description: Yup.string().required("Description required"),
  category: Yup.string().required("Category required"),
  location: Yup.string().required("Location required")
});

function PostItemForm() {
  const navigate = useNavigate();

  function handleSubmit(values, { setSubmitting }) {
    createItem(values).then(() => {
      alert("Item posted successfully!");
      navigate("/dashboard");
    }).catch(err => {
      console.error(err);
      alert("Failed to post item. Please try again.");
    }).finally(() => {
      setSubmitting(false);
    });
  }

  return (
    <div style={{ padding: "40px 20px", maxWidth: "800px", margin: "0 auto" }}>
      <div style={{
        background: "white",
        padding: "40px",
        borderRadius: "24px",
        boxShadow: "0 10px 40px rgba(0,0,0,0.05)",
        border: "1px solid #f0f0f0"
      }}>
        <div style={{ textAlign: "center", marginBottom: "40px" }}>
          <div style={{
            display: "inline-flex",
            background: "var(--accent-maroon)15",
            padding: "16px",
            borderRadius: "20px",
            marginBottom: "16px"
          }}>
            <Package size={32} color="var(--accent-maroon)" />
          </div>
          <h2 style={{ fontSize: "2rem", color: "var(--accent-maroon)", marginBottom: "8px" }}>Post a New Item</h2>
          <p style={{ color: "#666" }}>Share what you no longer need with someone who does.</p>
        </div>

        <Formik
          initialValues={{
            title: "",
            description: "",
            category: "",
            condition: "",
            location: "",
            pickup_days: "",
            pickup_times: "",
            photo_url: "",
            instructions: ""
          }}
          validationSchema={schema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form>
              <div style={gridStyle}>
                {/* Title */}
                <div style={fullWidthStyle}>
                  <label style={labelStyle}>
                    <Tag size={16} /> Item Title
                  </label>
                  <Field name="title" placeholder="What are you giving away?" className="form-input" />
                  <ErrorMessage name="title" component="div" style={errorStyle} />
                </div>

                {/* Description */}
                <div style={fullWidthStyle}>
                  <label style={labelStyle}>
                    <AlignLeft size={16} /> Description
                  </label>
                  <Field as="textarea" name="description" placeholder="Describe the item, its condition, and any other details..." style={{ ...inputStyle, minHeight: "120px", resize: "vertical" }} />
                  <ErrorMessage name="description" component="div" style={errorStyle} />
                </div>

                {/* Category */}
                <div style={halfWidthStyle}>
                  <label style={labelStyle}>
                    <Package size={16} /> Category
                  </label>
                  <Field as="select" name="category" className="form-input">
                    <option value="">Select Category</option>
                    <option value="Kitchen">Kitchen</option>
                    <option value="Furniture">Furniture</option>
                    <option value="Clothes">Clothes</option>
                    <option value="Books">Books</option>
                    <option value="Electronics">Electronics</option>
                    <option value="Other">Other</option>
                  </Field>
                  <ErrorMessage name="category" component="div" style={errorStyle} />
                </div>

                {/* Condition */}
                <div style={halfWidthStyle}>
                  <label style={labelStyle}>
                    <Info size={16} /> Condition
                  </label>
                  <Field name="condition" placeholder="e.g. Good, Like New" className="form-input" />
                </div>

                {/* Location */}
                <div style={fullWidthStyle}>
                  <label style={labelStyle}>
                    <MapPin size={16} /> Pickup Location
                  </label>
                  <Field name="location" placeholder="e.g. Westlands, Near Total Station" className="form-input" />
                  <ErrorMessage name="location" component="div" style={errorStyle} />
                </div>

                {/* Pickup Days */}
                <div style={halfWidthStyle}>
                  <label style={labelStyle}>
                    <Calendar size={16} /> Preferred Days
                  </label>
                  <Field name="pickup_days" placeholder="e.g. Weekends only" className="form-input" />
                </div>

                {/* Pickup Times */}
                <div style={halfWidthStyle}>
                  <label style={labelStyle}>
                    <Clock size={16} /> Preferred Times
                  </label>
                  <Field name="pickup_times" placeholder="e.g. 10 AM - 4 PM" className="form-input" />
                </div>

                {/* Photo URL */}
                <div style={fullWidthStyle}>
                  <label style={labelStyle}>
                    <ImageIcon size={16} /> Photo URL
                  </label>
                  <Field name="photo_url" placeholder="https://example.com/item-photo.jpg" className="form-input" />
                </div>

                {/* Special Instructions */}
                <div style={fullWidthStyle}>
                  <label style={labelStyle}>
                    <Info size={16} /> Special Instructions
                  </label>
                  <Field name="instructions" placeholder="Any other details about pickup..." className="form-input" />
                </div>
              </div>

              <div style={{ marginTop: "40px" }}>
                <button
                  type="submit"
                  className="btn-primary"
                  style={{ width: "100%", padding: "16px", fontSize: "1.1rem" }}
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Posting..." : "Post Item Now"}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}

const gridStyle = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "24px"
};

const fullWidthStyle = {
  gridColumn: "1 / -1"
};

const halfWidthStyle = {
  gridColumn: "span 1"
};

const labelStyle = {
  display: "flex",
  alignItems: "center",
  gap: "8px",
  marginBottom: "8px",
  fontWeight: "600",
  fontSize: "0.9rem",
  color: "#444"
};

const inputStyle = {
  width: "100%",
  padding: "12px 16px",
  borderRadius: "12px",
  border: "1px solid #e0e0e0",
  fontSize: "1rem",
  transition: "border-color 0.2s ease, box-shadow 0.2s ease",
  outline: "none"
};

const errorStyle = {
  color: "var(--accent-maroon)",
  fontSize: "0.8rem",
  marginTop: "4px",
  fontWeight: "500"
};

export default PostItemForm;