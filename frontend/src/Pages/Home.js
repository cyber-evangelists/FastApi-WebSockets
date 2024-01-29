import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import "./Home.css";

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const newWebSocket = new WebSocket("ws://localhost:8000/ws");

    newWebSocket.onopen = () => {
      console.log("WebSocket connection opened");
    };

    newWebSocket.onmessage = function (event) {
      setMessages((prevMessages) => [...prevMessages, JSON.parse(event.data)]);
    };

    setWs(newWebSocket);

    return () => {
      newWebSocket.close();
    };
  }, []);
  const formik = useFormik({
    initialValues: {
      postId: "",
      title: "",
      postText: "",
      deleteID: "",
    },
    onSubmit: () => {},
    validate: (values) => {
      const errors = {};
      return errors;
    },
  });

  const handleRead = (event) => {
    ws.send("get_all_posts");
    event.preventDefault();
  };

  const handleGetPostById = (event) => {
    if (!formik.values.postId) {
      alert("Please enter id.");
    } else if (/[^\w\d]/.test(formik.values.postId)) {
      alert("ID cannot contain special characters");
    } else {
      ws.send("get_post_by_id:" + formik.values.postId);
    }

    event.preventDefault();
  };
  const handleAddPost = (event) => {
    if (!formik.values.title || !formik.values.postText) {
      alert("Title and Post Text are required.");
    } else if (
      /\d|[@$!%^&*()_+|~=`{}\[\]:";'<>?,.\/]/.test(formik.values.title)
    ) {
      alert("Title cannot contain numbers or special characters.");
    } else {
      ws.send(
        "add_post:" + ":" + formik.values.title + ":" + formik.values.postText
      );
    }
    event.preventDefault();
  };
  const handleDelete = (event) => {
    if (!formik.values.deleteID) {
      alert("Please enter id.");
    } else if (/[^\w\d]/.test(formik.values.deleteID)) {
      alert("ID cannot contain special characters");
    } else {
      ws.send("delete_post:" + formik.values.deleteID);
    }
    event.preventDefault();
  };

  return (
    <div>
      <div className="container form">
        <h1>Websocket CRUD</h1>
        <div className="searchpost row">
          <label htmlFor="postId">Search a Post:</label>
          <input
            type="text"
            id="postId"
            name="postId"
            value={formik.values.postId}
            onChange={formik.handleChange}
            required
            placeholder="Enter Post ID"
          />
          <button onClick={handleGetPostById} type="submit">
            Get Post by ID
          </button>
          {formik.errors.postId && <div>{formik.errors.postId}</div>}
        </div>
        <div className="addpost row">
          <label htmlFor="title">Add a new Post:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formik.values.title}
            onChange={formik.handleChange}
            required
            pattern="[A-Za-z\s]+"
            placeholder="Enter Title"
          />

          <input
            type="text"
            id="postText"
            name="postText"
            value={formik.values.postText}
            onChange={formik.handleChange}
            required
            pattern="[A-Za-z\s]+"
            placeholder="Enter Post Text"
          />
          <button onClick={handleAddPost} type="submit">
            Add a new post
          </button>
          {formik.errors.title && <div>{formik.errors.title}</div>}
          {formik.errors.postText && <div>{formik.errors.postText}</div>}
        </div>
        <div className="row">
          <button onClick={handleRead} id="getpostsbyID">
            Get all posts
          </button>
        </div>
        <div className="row">
          <input
            type="text"
            id="deleteID"
            name="deleteID"
            required
            value={formik.values.deleteID}
            onChange={formik.handleChange}
            pattern="[A-Za-z\s]+"
            placeholder="Enter ID to Delete"
          />
          <button onClick={handleDelete} id="delteID">
            Delete post
          </button>
        </div>
      </div>
      <div className="container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Text</th>
            </tr>
          </thead>
          <tbody>
            {messages.map((message, index) => (
              <tr key={index}>
                <td>{message._id}</td>
                <td>{message.title}</td>
                <td>{message.text}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {/* <ul>
        {messages.map((message, index) => (
          <li key={index}>
            {message._id}
            {message.title}
            {message.text}
          </li>
        ))}
      </ul> */}
      </div>
    </div>
  );
};

export default Home;
