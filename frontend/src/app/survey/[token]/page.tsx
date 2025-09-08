"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { surveyApi } from "@/lib/api/client";
import { Question, CreateAnswerRequest } from "@/lib/api/types";

interface Answer {
  question_id: string;
  selected_options?: string[];
  text_answer?: string;
  number_answer?: number;
}

export default function SurveyPage() {
  const params = useParams();
  const router = useRouter();
  const token = params.token as string;
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState<Answer | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Load real questions from API
  useEffect(() => {
    const loadQuestions = async () => {
      try {
        const loadedQuestions = await surveyApi.getQuestions(token);
        setQuestions(loadedQuestions);
      } catch (error) {
        console.error("Error loading questions:", error);
      } finally {
        setIsLoading(false);
      }
    };

    if (token) {
      loadQuestions();
    }
  }, [token]);

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  const handleAnswerChange = (value: string | string[]) => {
    if (!currentQuestion) return;

    const answer: Answer = {
      question_id: currentQuestion.id,
    };

    switch (currentQuestion.type) {
      case "single_choice":
        answer.selected_options = [value as string];
        break;
      case "multiple_choice":
        answer.selected_options = value as string[];
        break;
      case "text":
        answer.text_answer = value as string;
        break;
      case "number":
        answer.number_answer = parseInt(value as string);
        break;
    }

    setCurrentAnswer(answer);
  };

  const handleNext = async () => {
    if (!currentAnswer && currentQuestion.is_required) return;

    setIsSubmitting(true);
    
    try {
      // Submit answer to backend
      if (currentAnswer) {
        const submitRequest: CreateAnswerRequest = {
          question_id: currentAnswer.question_id,
          text_answer: currentAnswer.text_answer,
          number_answer: currentAnswer.number_answer,
          selected_option_ids: currentAnswer.selected_options
        };
        await surveyApi.submitAnswer(token, submitRequest);
        
        // Save answer locally
        setAnswers(prev => {
          const newAnswers = prev.filter(a => a.question_id !== currentAnswer.question_id);
          return [...newAnswers, currentAnswer];
        });
      }

      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(prev => prev + 1);
        setCurrentAnswer(null);
      } else {
        // Complete survey
        await surveyApi.completeSurvey(token);
        setIsCompleted(true);
      }
    } catch (error) {
      console.error("Error submitting answer:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
      // Load previous answer
      const prevAnswer = answers.find(a => a.question_id === questions[currentQuestionIndex - 1].id);
      setCurrentAnswer(prevAnswer || null);
    }
  };

  const handleViewResults = () => {
    router.push(`/results/${token}`);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Загружаем вопросы...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (isCompleted) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-green-600 text-2xl">✓</span>
            </div>
            <CardTitle className="text-2xl">Спасибо за участие!</CardTitle>
            <CardDescription className="text-lg">
              Вы успешно прошли опрос. Ваши ответы сохранены.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button onClick={handleViewResults} className="mt-4">
              Посмотреть мои ответы
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardContent className="p-8 text-center">
            <p className="text-destructive">Ошибка загрузки вопроса</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-2xl mx-auto py-8">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-muted-foreground">
              Вопрос {currentQuestionIndex + 1} из {questions.length}
            </span>
            <span className="text-sm text-muted-foreground">
              {Math.round(progress)}%
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="text-xl">
              {currentQuestion.text}
              {currentQuestion.is_required && <span className="text-destructive ml-1">*</span>}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {currentQuestion.type === "single_choice" && (
              <div className="space-y-2">
                {currentQuestion.options?.map((option) => (
                  <div key={option.id} className="flex items-center space-x-2">
                    <input
                      type="radio"
                      id={option.id.toString()}
                      name="single-choice"
                      value={option.id.toString()}
                      checked={currentAnswer?.selected_options?.[0] === option.id.toString()}
                      onChange={(e) => handleAnswerChange(e.target.value)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <Label htmlFor={option.id.toString()} className="cursor-pointer">
                      {option.text}
                    </Label>
                  </div>
                ))}
              </div>
            )}

            {currentQuestion.type === "multiple_choice" && (
              <div className="space-y-2">
                {currentQuestion.options?.map((option) => (
                  <div key={option.id} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id={option.id.toString()}
                      checked={currentAnswer?.selected_options?.includes(option.id.toString()) || false}
                      onChange={(e) => {
                        const currentSelection = currentAnswer?.selected_options || [];
                        const newSelection = e.target.checked
                          ? [...currentSelection, option.id.toString()]
                          : currentSelection.filter(id => id !== option.id.toString());
                        handleAnswerChange(newSelection);
                      }}
                      className="rounded border-gray-300"
                    />
                    <Label htmlFor={option.id.toString()} className="cursor-pointer">
                      {option.text}
                    </Label>
                  </div>
                ))}
              </div>
            )}

            {currentQuestion.type === "text" && (
              <textarea
                className="w-full p-3 border border-input rounded-md resize-none"
                rows={4}
                placeholder="Введите ваш ответ..."
                value={currentAnswer?.text_answer || ""}
                onChange={(e) => handleAnswerChange(e.target.value)}
              />
            )}

            {currentQuestion.type === "number" && (
              <Input
                type="number"
                placeholder="Введите число..."
                value={currentAnswer?.number_answer?.toString() || ""}
                onChange={(e) => handleAnswerChange(e.target.value)}
              />
            )}

            <div className="flex justify-between pt-6">
              <Button
                variant="outline"
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
              >
                ← Назад
              </Button>
              
              <Button
                onClick={handleNext}
                disabled={
                  isSubmitting || 
                  (currentQuestion.is_required && !currentAnswer)
                }
              >
                {isSubmitting ? "Сохраняем..." : 
                 currentQuestionIndex === questions.length - 1 ? "Завершить" : "Далее →"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}