"use client";

import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { surveyApi } from "@/lib/api/client";

export default function Home() {
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsSubmitting(true);
    setError(null);
    
    try {
      await surveyApi.submitEmail(email);
      setIsSubmitted(true);
    } catch (error) {
      console.error("Error submitting email:", error);
      setError("Произошла ошибка при отправке email. Попробуйте еще раз.");
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-green-600 text-xl">✉</span>
            </div>
            <CardTitle>Письмо отправлено!</CardTitle>
            <CardDescription>
              Мы отправили ссылку на опрос на ваш email {email}. 
              Проверьте почту и следуйте инструкциям.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 to-indigo-100">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Survey API</CardTitle>
          <CardDescription className="text-lg">
            Участвуйте в нашем исследовании и делитесь своим мнением
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email адрес</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isSubmitting}
              />
            </div>
            {error && (
              <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
                {error}
              </div>
            )}
            <Button 
              type="submit" 
              className="w-full" 
              disabled={isSubmitting || !email}
            >
              {isSubmitting ? "Отправляем..." : "Участвовать в опросе"}
            </Button>
          </form>
          <div className="mt-6 text-center text-sm text-muted-foreground">
            <p>Мы отправим вам ссылку на опрос по электронной почте.</p>
            <p className="mt-2">Ваши данные защищены и не будут переданы третьим лицам.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
