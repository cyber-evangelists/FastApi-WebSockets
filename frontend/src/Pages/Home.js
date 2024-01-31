import React, { useState, useEffect } from "react";
import "./Home.css";

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const newWebSocket = new WebSocket("ws://localhost:8000/ws");

    newWebSocket.onopen = () => {
      console.log("WebSocket connection opened");
    };
    const MessageType = {
      INVALID: "invalid",
      INSERTED: "inserted",
      DELETED: "deleted",
      NOT_DELETED: "not deleted",
      NOT_EXIST: "not exist",
    };

    newWebSocket.onmessage = function (event) {
      const data = event.data;
      handleMessage(data);
    };
    const alertMessages = {
      [MessageType.INVALID]: "Post with this ID does not exist",
      [MessageType.INSERTED]: "Your post has been inserted successfully",
      [MessageType.DELETED]: "Post has been deleted successfully",
      [MessageType.NOT_DELETED]: "Your post could not be deleted",
      [MessageType.NOT_EXIST]: "You have entered an invalid ID",
    };
    function handleMessage(data) {
      const message = alertMessages[data];
      if (message) {
        displayAlert(message);
      } else {
        setMessages((prevMessages) => [...prevMessages, JSON.parse(data)]);
      }
    }
    function displayAlert(message) {
      alert(message);
    }
    setWs(newWebSocket);

    return () => {
      newWebSocket.close();
    };
  }, []);
  const ACTIONS = {
    GET_ALL_POSTS: "get_all_posts",
    GET_POST_BY_ID: "get_post_by_id",
    ADD_POST: "add_post:",
    DELETE_POST: "delete_post",
  };
  const handleRead = (event) => {
    setMessages([]);
    ws.send(ACTIONS.GET_ALL_POSTS);
    event.preventDefault();
  };

  const handleGetPostById = (event) => {
    if (!formData.searchID) {
      alert("ID cannot b empty");
      return;
    } else {
      setMessages([]);
      ws.send(`${ACTIONS.GET_POST_BY_ID}:${formData.searchID}`);
    }

    event.preventDefault();
  };
  const handleAddPost = (event) => {
    if (!formData.postText || !formData.postTitle) {
      alert("Post Title or Text cannot be empty");
      return;
    } else {
      ws.send(`${ACTIONS.ADD_POST}:${formData.postTitle}:${formData.postText}`);
      setMessages([]);
      ws.send(ACTIONS.GET_ALL_POSTS);
    }
    event.preventDefault();
  };
  const handleDelete = (event) => {
    if (!formData.deleteID) {
      alert("Please enter ID.");
    } else {
      ws.send(`${ACTIONS.DELETE_POST}:${formData.deleteID}`);
      setMessages([]);
      ws.send(ACTIONS.GET_ALL_POSTS);
    }
    event.preventDefault();
  };
  const [formData, setFormData] = useState({
    postText: "",
    postTitle: "",
    deleteID: "",
    searchID: "",
  });
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === "postTitle" && !/^[a-zA-Z\s]*$/.test(value)) {
      alert("Please enter valid Title");

      return;
    }
    if (name === "postText" && !/^[a-zA-Z\s]*$/.test(value)) {
      alert("Please enter valid Text");
      return;
    }
    if (name === "searchID" && !/^[a-zA-Z0-9]*$/.test(value)) {
      alert("Please enter valid ID");
      return;
    }
    if (name === "deleteID" && !/^[a-zA-Z0-9]*$/.test(value)) {
      alert("Please enter valid ID");
      return;
    }
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <div>
      <div className="container form">
        <h1>Websocket CRUD</h1>
        <form onSubmit={handleGetPostById}>
          <div className="searchpost row">
            <label htmlFor="postId">Search a Post:</label>
            <input
              type="text"
              id="searchID"
              name="searchID"
              value={formData.searchID}
              onChange={handleInputChange}
              placeholder="Enter Post ID"
            />
            <button type="submit">Get Post by ID</button>
          </div>
        </form>
        <form onSubmit={handleAddPost}>
          <div className="addpost row">
            <label htmlFor="title">Add a new Post:</label>
            <input
              type="text"
              id="postTitle"
              name="postTitle"
              value={formData.postTitle}
              onChange={handleInputChange}
              placeholder="Enter Title"
            />

            <input
              type="text"
              id="postText"
              name="postText"
              value={formData.postText}
              onChange={handleInputChange}
              placeholder="Enter Post Text"
            />
            <button type="submit">Add a new post</button>
          </div>
        </form>

        <div className="row">
          <button onClick={handleRead} id="getpostsbyID">
            Get all posts
          </button>
        </div>
        <form onSubmit={handleDelete}>
          <div className="row">
            <input
              type="text"
              id="deleteID"
              name="deleteID"
              value={formData.deleteID}
              onChange={handleInputChange}
              placeholder="Enter ID to Delete"
            />
            <button type="submit" id="delteID">
              Delete post
            </button>
          </div>
        </form>
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
      </div>
    </div>
  );
};

export default Home;
