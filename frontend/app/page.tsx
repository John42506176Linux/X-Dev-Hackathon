"use client"
import Link from "next/link"
import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { siteConfig } from "@/config/site"
import { buttonVariants } from "@/components/ui/button"
import {useEffect} from "react";

export default function IndexPage() {
  useEffect(() => {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/3293358400');

    socket.onopen = () => {
      console.log('WebSocket connection established');
  //     const sendMessage = (data = 3293358400) => {
  //     socket.send(JSON.stringify(data));
  // };

    };
    socket.onmessage = (event) => {
    const data = JSON.parse(event.data); // Assuming JSON data
    // Update your React state based on the received data
      console.log(data)
  };

    // ... other event handlers below

    return () => {
            if (socket.readyState === 1) { // <-- This is important
                socket.close();
            }
        }
  }, []);
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
        </div>
      </div>
      {/*<div className="hidden bg-muted lg:block">*/}
      {/*  <Image*/}
      {/*    src="/placeholder.svg"*/}
      {/*    alt="Image"*/}
      {/*    width="1920"*/}
      {/*    height="1080"*/}
      {/*    className="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"*/}
      {/*  />*/}
      {/*</div>*/}
    </div>
  )
}
