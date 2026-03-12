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
    <div style={{ marginTop: "20px", borderTop: "1px solid gray", paddingTop: "20px" }}>

      <h3>Request This Item</h3>

      <Formik
        initialValues={{
          message: "",
          confirm: false
        }}
        validationSchema={schema}
        onSubmit={handleSubmit}
      >

        <Form>

          <div>
            <label>Message to Giver</label><br/>
            <Field
              as="textarea"
              name="message"
              placeholder="Write a short message..."
            />
            <br/>
            <ErrorMessage name="message" component="div" style={{color:"red"}}/>
          </div>

          <div style={{marginTop:"10px"}}>
            <label>
              <Field type="checkbox" name="confirm"/>
              {" "}I confirm I can follow the pickup terms
            </label>
            <br/>
            <ErrorMessage name="confirm" component="div" style={{color:"red"}}/>
          </div>

          <button type="submit" style={{marginTop:"10px"}}>
            Send Request
          </button>

        </Form>

      </Formik>

    </div>
  );
}

export default RequestForm; 