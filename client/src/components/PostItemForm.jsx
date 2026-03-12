import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { createItem } from "../api/api";

const schema = Yup.object({
  title: Yup.string().required("Title required"),
  description: Yup.string().required("Description required"),
  category: Yup.string().required("Category required"),
  location: Yup.string().required("Location required")
});

function PostItemForm() {

  function handleSubmit(values, {resetForm}) {
    createItem(values).then(() => {
      alert("Item posted successfully");
      resetForm();
    });
  }

  return (
    <div>
      <h2>Post Item</h2>

      <Formik
        initialValues={{
          title:"",
          description:"",
          category:"",
          condition:"",
          location:"",
          pickup_days:"",
          pickup_times:"",
          photo_url:"",
          instructions:""
        }}
        validationSchema={schema}
        onSubmit={handleSubmit}
      >

        <Form>

          <div>
            <label>Title</label>
            <Field name="title"/>
            <ErrorMessage name="title"/>
          </div>

          <div>
            <label>Description</label>
            <Field name="description"/>
            <ErrorMessage name="description"/>
          </div>

          <div>
            <label>Category</label>
            <Field as="select" name="category">
              <option value="">Select</option>
              <option value="Kitchen">Kitchen</option>
              <option value="Furniture">Furniture</option>
              <option value="Clothes">Clothes</option>
              <option value="Books">Books</option>
              <option value="Electronics">Electronics</option>
            </Field>
            <ErrorMessage name="category"/>
          </div>

          <div>
            <label>Condition</label>
            <Field name="condition"/>
          </div>

          <div>
            <label>Location</label>
            <Field name="location"/>
            <ErrorMessage name="location"/>
          </div>

          <div>
            <label>Pickup Days</label>
            <Field name="pickup_days"/>
          </div>

          <div>
            <label>Pickup Times</label>
            <Field name="pickup_times"/>
          </div>

          <div>
            <label>Photo URL</label>
            <Field name="photo_url"/>
          </div>

          <div>
            <label>Instructions</label>
            <Field name="instructions"/>
          </div>

          <button type="submit">Post Item</button>

        </Form>

      </Formik>

    </div>
  );
}

export default PostItemForm; 