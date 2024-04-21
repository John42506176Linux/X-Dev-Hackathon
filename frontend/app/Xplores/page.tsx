"use client"
import React, {
  useEffect,
  useState
} from "react";
// @ts-ignore
import {
  Box,
  Button,
  Flex,
  Input,
  InputGroup,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Stack,
  Text,
  useDisclosure
} from "@chakra-ui/react";

const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})

export default function Todos() {
  const [todos, setTodos] = useState([])
  const fetchTodos = async () => {
    // const response = await fetch("http://localhost:8000/initial_topics/3293358400")
    try {
      const response = await fetch("http://localhost:8000/initial_topics/3293358400");

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }

      const todos = await response.json();

      console.log("How many:", todos); // Assuming todos is an array
      setTodos(todos.data)
    } catch (error) {
      console.error("There was an error fetching todos:", error);
    }
    //
  }
  useEffect(() => {
    fetchTodos()
  }, [])
  // @ts-ignore
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <Stack spacing={5}>
        {/*{todos.map((todo) => (*/}
        {/*  <b>{todo.item}</b>*/}
        {/*))}*/}
      </Stack>
    </TodosContext.Provider>
  )
}
