// @ts-nocheck
"use client"
import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { siteConfig } from "@/config/site"
import { buttonVariants } from "@/components/ui/button"
import {useEffect, useState} from "react";

export default function IndexPage() {
  const [formData, setFormData] = useState({
    handle: '',
  });

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.handle]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    localStorage.setItem('formData', JSON.stringify(formData));
    console.log('Form data saved to localStorage!');
    try {
      // ... Send data to API, await response
      window.location.href = '/Xplore';
    } catch (error) {
      console.log(error)  // Redirect to an error page
    }
  };
  return (
    // <div className="w-full lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px]">
    <div className="w-full lg:grid lg:min-h-[600px] lg:grid-cols-1 xl:min-h-[800px]">
      <div className="flex items-center justify-center pb-12">
        <div className="mx-auto grid w-[350px] gap-6">
          <div className="grid gap-2 text-center">
            <h1 className="text-3xl font-bold">Welcome.</h1>
            <p className="text-balance text-muted-foreground">
              Enter your X handle below.
            </p>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                {/*<Label htmlFor="handle">Handle</Label>*/}
                <Input
                  id="handle"
                  type="text"
                  placeholder="@laptopcrust"
                  required
                />
              </div>
              <Button type="submit" className="w-full">
                Explore
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
)
}


