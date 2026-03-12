import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  phone: Yup.string()
    .matches(/^(07|01)\d{8}$/, "Invalid Kenyan phone number")
    .required("Phone required"),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password required")
});

function Login() {

  function handleSubmit(values) {
    console.log("Login data:", values);
  }

  return (

    <div>

      <h2>Login</h2>

      <Formik
        initialValues={{
          phone: "",
          password: ""
        }}
        validationSchema={schema}
        onSubmit={handleSubmit}
      >

        <Form>

          <div>
            <label>Phone</label>
            <Field name="phone"/>
            <ErrorMessage name="phone"/>
          </div>

          <div>
            <label>Password</label>
            <Field type="password" name="password"/>
            <ErrorMessage name="password"/>
          </div>

          <button type="submit">Login</button>

        </Form>

      </Formik>

    </div>

  );
}

export default Login;