import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { createRequest } from "../api/api";

const schema = Yup.object({
  message: Yup.string().required("Message is required"),
  confirm: Yup.boolean().oneOf([true], "You must confirm pickup terms")
});

function RequestForm({ itemId }) {

  function handleSubmit(values, { resetForm }) {
    createRequest(itemId, values.message)
      .then(() => {
        alert("Request sent successfully!");
        resetForm();
      })
      .catch(() => {
        alert("Failed to send request");
      });
  }

  return (
    <div style={{ marginTop: "24px", color: "var(--neutral-black)" }}>
      <Formik
        initialValues={{
          message: "",
          confirm: false
        }}
        validationSchema={schema}
        onSubmit={handleSubmit}
      >
        <Form>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "600", fontSize: "0.9rem" }}>
              Message to Giver
            </label>
            <Field
              as="textarea"
              name="message"
              placeholder="Tell the giver why you need this or when you can pick it up..."
              style={{ minHeight: "100px", resize: "vertical" }}
            />
            <ErrorMessage name="message" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "-10px" }} />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "flex", alignItems: "flex-start", gap: "10px", fontSize: "0.9rem", cursor: "pointer" }}>
              <Field type="checkbox" name="confirm" style={{ width: "auto", margin: "4px 0 0 0" }} />
              <span>I confirm that I can follow the pickup terms and will handle the item with care.</span>
            </label>
            <ErrorMessage name="confirm" component="div" style={{ color: "var(--accent-maroon)", fontSize: "0.8rem", marginTop: "4px" }} />
          </div>

          <button type="submit" className="btn-primary" style={{ width: "100%", padding: "14px" }}>
            Send Request
          </button>
        </Form>
      </Formik>
    </div>
  );
}

export default RequestForm;