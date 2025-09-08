"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Question {
  id: number;
  text: string;
  type: "single_choice" | "multiple_choice" | "text" | "number";
  options?: { id: number; text: string }[];
}

interface Answer {
  question_id: number;
  selected_options?: number[];
  text_answer?: string;
  number_answer?: number;
  question: Question;
}

interface UserSurveyResults {
  user_email: string;
  survey_title: string;
  completed_at: string;
  answers: Answer[];
}

export default function ResultsPage() {
  const params = useParams();
  const token = params.token as string;
  
  const [results, setResults] = useState<UserSurveyResults | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        // Mock data - replace with actual API call
        const mockResults: UserSurveyResults = {
          user_email: "user@example.com",
          survey_title: "Опрос разработчиков 2024",
          completed_at: "2024-01-15T10:30:00Z",
          answers: [
            {
              question_id: 1,
              selected_options: [2],
              question: {
                id: 1,
                text: "Какой ваш основной язык программирования?",
                type: "single_choice",
                options: [
                  { id: 1, text: "JavaScript" },
                  { id: 2, text: "Python" },
                  { id: 3, text: "Java" },
                  { id: 4, text: "C#" },
                  { id: 5, text: "Go" },
                ],
              },
            },
            {
              question_id: 2,
              number_answer: 5,
              question: {
                id: 2,
                text: "Сколько лет вы программируете?",
                type: "number",
              },
            },
            {
              question_id: 3,
              selected_options: [6, 9, 11],
              question: {
                id: 3,
                text: "Какие фреймворки вы используете? (выберите несколько)",
                type: "multiple_choice",
                options: [
                  { id: 6, text: "React" },
                  { id: 7, text: "Vue.js" },
                  { id: 8, text: "Angular" },
                  { id: 9, text: "Django" },
                  { id: 10, text: "Flask" },
                  { id: 11, text: "FastAPI" },
                ],
              },
            },
            {
              question_id: 4,
              text_answer: "Я работаю full-stack разработчиком уже 5 лет. Начинал с Python и Django, потом добавил React для фронтенда. Недавно начал изучать FastAPI - очень нравится его простота и производительность.",
              question: {
                id: 4,
                text: "Расскажите о своем опыте разработки",
                type: "text",
              },
            },
          ],
        };

        await new Promise(resolve => setTimeout(resolve, 800));
        setResults(mockResults);
      } catch (err) {
        setError("Не удалось загрузить результаты опроса");
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, [token]);

  const getAnswerIcon = (type: string) => {
    switch (type) {
      case "single_choice":
        return <span className="text-xs">◉</span>;
      case "multiple_choice":
        return <span className="text-xs">☑</span>;
      case "text":
        return <span className="text-xs">📝</span>;
      case "number":
        return <span className="text-xs">#</span>;
      default:
        return null;
    }
  };

  const renderAnswer = (answer: Answer) => {
    const { question } = answer;

    switch (question.type) {
      case "single_choice":
        const selectedOption = question.options?.find(
          option => answer.selected_options?.includes(option.id)
        );
        return (
          <Badge variant="secondary" className="text-sm">
            {selectedOption?.text || "Не выбрано"}
          </Badge>
        );

      case "multiple_choice":
        const selectedOptions = question.options?.filter(
          option => answer.selected_options?.includes(option.id)
        ) || [];
        return (
          <div className="flex flex-wrap gap-2">
            {selectedOptions.map(option => (
              <Badge key={option.id} variant="secondary" className="text-sm">
                {option.text}
              </Badge>
            ))}
            {selectedOptions.length === 0 && (
              <Badge variant="outline" className="text-sm">
                Не выбрано
              </Badge>
            )}
          </div>
        );

      case "text":
        return (
          <div className="bg-muted p-3 rounded-md text-sm">
            {answer.text_answer || "Нет ответа"}
          </div>
        );

      case "number":
        return (
          <Badge variant="secondary" className="text-sm">
            {answer.number_answer ?? "Не указано"}
          </Badge>
        );

      default:
        return <span className="text-muted-foreground">Неизвестный тип ответа</span>;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Загружаем ваши ответы...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardHeader className="text-center">
            <CardTitle className="text-destructive">Ошибка</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardHeader className="text-center">
            <CardTitle>Результаты не найдены</CardTitle>
            <CardDescription>
              Не удалось найти результаты опроса для данного токена.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto py-8">
        <Card className="mb-8">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Ваши ответы</CardTitle>
            <CardDescription className="text-lg">
              {results.survey_title}
            </CardDescription>
            <div className="flex justify-center items-center gap-4 mt-4 text-sm text-muted-foreground">
              <span>Email: {results.user_email}</span>
              <span>•</span>
              <span>
                Завершено: {new Date(results.completed_at).toLocaleDateString('ru-RU', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
          </CardHeader>
        </Card>

        <div className="space-y-6">
          {results.answers.map((answer, index) => (
            <Card key={answer.question_id}>
              <CardHeader>
                <div className="flex items-start gap-3">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <span className="text-sm font-medium">#{index + 1}</span>
                    {getAnswerIcon(answer.question.type)}
                  </div>
                  <div className="flex-1">
                    <CardTitle className="text-lg font-medium">
                      {answer.question.text}
                    </CardTitle>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {renderAnswer(answer)}
              </CardContent>
            </Card>
          ))}
        </div>

        <Card className="mt-8">
          <CardContent className="p-6 text-center text-muted-foreground">
            <p className="text-sm">
              Спасибо за участие в нашем опросе! Ваши ответы помогут нам лучше понимать 
              потребности разработчиков и улучшать наши продукты.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}