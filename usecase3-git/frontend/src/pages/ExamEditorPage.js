import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { getExam } from "../api";
import AddQuestionForm from "../components/AddQuestionForm";
import QuestionList from "../components/QuestionList";
import OptionsForm from "../components/OptionsForm";

export default function ExamEditorPage() {
  const { id } = useParams();
  const [exam, setExam] = useState(null);

  useEffect(() => { getExam(id).then(setExam); }, [id]);

  if (!exam) return <p>Loading...</p>;

  return (
    <>
      <h2>Editing: {exam.title}</h2>
      <OptionsForm exam={exam} />
      <AddQuestionForm examId={exam.exam_id} onAdded={() => getExam(id).then(setExam)} />
      <QuestionList questions={exam.questions} />
    </>
  );
}
