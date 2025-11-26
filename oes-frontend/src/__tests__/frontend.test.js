import "@testing-library/jest-dom";
jest.mock("axios");

import axios from "axios";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

// Pages
import ExamSetup from "../pages/ExamSetup";
import InstructorDashboard from "../pages/InstructorDashboard";
import ExamEditor from "../pages/ExamEditor";

function Wrapper({ children }) {
  return <BrowserRouter>{children}</BrowserRouter>;
}

// TESTS FOR ExamSetup.js

test("ExamSetup loads input fields correctly", () => {
  render(<ExamSetup />, { wrapper: Wrapper });

  expect(screen.getByLabelText(/Course Code/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/Instructor Email/i)).toBeInTheDocument();
  expect(screen.getByText(/Create Exam/i)).toBeInTheDocument();
});

test("ExamSetup shows error if inputs are empty", async () => {
  render(<ExamSetup />, { wrapper: Wrapper });

  fireEvent.click(screen.getByText(/Create Exam/i));

  expect(await screen.findByText(/required/i)).toBeInTheDocument();
});

test("ExamSetup sends POST request and redirects", async () => {
  axios.post.mockResolvedValue({
    data: { exam_id: 5 }
  });

  render(<ExamSetup />, { wrapper: Wrapper });

  fireEvent.change(screen.getByLabelText(/Course Code/i), {
    target: { value: "CS101" }
  });

  fireEvent.change(screen.getByLabelText(/Instructor Email/i), {
    target: { value: "teacher@uni.com" }
  });

  fireEvent.click(screen.getByText(/Create Exam/i));

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalled();
  });
});

// TESTS FOR InstructorDashboard.js

test("InstructorDashboard loads exams", async () => {
  axios.get.mockResolvedValue({
    data: [
      { exam_id: 1, title: "Midterm", course_code: "CS101" },
      { exam_id: 2, title: "Final", course_code: "CS102" }
    ]
  });

  render(<InstructorDashboard />, { wrapper: Wrapper });

  fireEvent.click(screen.getByText(/Load Exams/i));

  expect(await screen.findByText(/Midterm/i)).toBeInTheDocument();
  expect(await screen.findByText(/Final/i)).toBeInTheDocument();
});

// TESTS FOR ExamEditor.js

test("ExamEditor loads questions", async () => {
  axios.get.mockResolvedValue({
    data: {
      questions: [
        {
          question_id: 10,
          question_text: "What is 2 + 2?",
          options: [{ option_text: "4", is_correct: 1 }]
        }
      ]
    }
  });

  render(<ExamEditor />, { wrapper: Wrapper });

  expect(await screen.findByText(/What is 2 \+ 2/i)).toBeInTheDocument();
});

test("ExamEditor opens Add Question modal", async () => {
    axios.get.mockResolvedValue({
      data: { questions: [] }
    });
  
    render(<ExamEditor />, { wrapper: Wrapper });
  
    // wait for the button "+ Add Question"
    const addBtn = await screen.findByRole("button", { name: /\+ Add Question/i });
    fireEvent.click(addBtn);
  
    // modal heading "Add Question"
    expect(await screen.findByText(/^Add Question$/i)).toBeInTheDocument();
  });
  

test("ExamEditor adds a question", async () => {
  axios.get.mockResolvedValue({ data: { questions: [] } });
  axios.post.mockResolvedValue({ data: { question_id: 20 } });

  render(<ExamEditor />, { wrapper: Wrapper });

  await screen.findByText(/Add Question/i);

  fireEvent.click(screen.getByText(/Add Question/i));

  fireEvent.change(screen.getByLabelText(/Question Text/i), {
    target: { value: "Sample question" }
  });

  const optionInput = screen.getAllByRole("textbox")[1];
  fireEvent.change(optionInput, {
    target: { value: "Option A" }
  });

  fireEvent.click(screen.getByText(/Save Question/i));

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalled();
  });
});
