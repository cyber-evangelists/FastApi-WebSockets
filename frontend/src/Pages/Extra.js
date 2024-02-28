// import React, { useState } from "react";

// const New = () => {
//   const [formData, setFormData] = useState({
//     name: "",
//     email: "",
//   });

//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     if (name === "name" && !/^[a-zA-Z\s]*$/.test(value)) {
//       alert("Please enter valid name");
//       return;
//     }
//     if (name === "email" && !/^[a-zA-Z\s]*$/.test(value)) {
//       alert("Please enter valid email");
//       return;
//     }
//     setFormData({
//       ...formData,
//       [name]: value,
//     });
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     console.log("Form submitted:", formData);
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <label>
//         Name:
//         <input
//           type="text"
//           name="name"
//           value={formData.name}
//           onChange={handleInputChange}
//         />
//       </label>
//       <br />
//       <label>
//         Email:
//         <input
//           type="text"
//           name="email"
//           value={formData.email}
//           onChange={handleInputChange}
//         />
//       </label>
//       <br />
//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default New;
