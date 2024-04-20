'use client'

import * as React from "react"
import Image from "next/image"

// @ts-ignore
import {ScrollArea, ScrollBar} from '@/components/ui/scroll-area'

export interface Artwork {
  artist: string
  art: string
}

export interface Tweet {
  profilePic: string
  userName: string
  handle: string
  content: string
  timestamp: string
}

export const tweets: Tweet[] = [
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: "$GMale",
    handle: "laptopcrust",
    content: "thinkin of my next tweet",
    timestamp: "Today at 3:32 PM"
  },
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: "$GMale",
    handle: "laptopcrust",
    content: "thinkin of my next tweet",
    timestamp: "Today at 3:32 PM"
  },
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: "$GMale",
    handle: "laptopcrust",
    content: "thinkin of my next tweet",
    timestamp: "Today at 3:32 PM"
  },
]
export const works: Artwork[] = [
  {
    artist: "Ornella Binni",
    art: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
  },
  {
    artist: "Tom Byrom",
    art: "https://images.unsplash.com/photo-1548516173-3cabfa4607e9?auto=format&fit=crop&w=300&q=80",
  },
  {
    artist: "Vladimir Malyavko",
    art: "https://images.unsplash.com/photo-1494337480532-3725c85fd2ab?auto=format&fit=crop&w=300&q=80",
  },
]

class SocialMediaPost extends React.Component<({ profilePic: any, userName: any, handle: any, content: any, timestamp: any })> {
  render() {
    let {profilePic, userName, handle, content, timestamp} = this.props;
    return (
      <div className="flex border border-gray-200 p-4 rounded-lg mb-5">
        <img
          src={profilePic}
          alt={`${userName}'s profile pic`}
          className="w-12 h-12 rounded-full mr-4"
        />
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="font-bold mr-2">{userName}</span>
            <span className="text-gray-500">{handle}</span>
          </div>
          <p>{content}</p>
          <span className="text-gray-500 text-sm">{timestamp}</span>
        </div>
      </div>
    );
  }
}

const postData = {
  profilePic: '...', // Replace with actual image URL
  userName: 'Twitter',
  handle: '@Twitter',
  content: 'Happy 3rd anniversary #TBT! See how "Throwback Thursday" cemented its status as a weekly Twitter tradition:',
  timestamp: '6:26 PM - Apr 30, 2015',
};
export default function ExplorePage() {
  return (
    <ScrollArea className="w-full whitespace-nowrap rounded-md border">
      {/*<div className="flex w-max space-x-4 p-4">*/}
      <div className="flex w-max space-x-4 p-4">
        {works.map((artwork) => (
          <figure key={artwork.artist} className="shrink-0">
            <div className="overflow-hidden rounded-md">
              <Image
                src={artwork.art}
                alt={`Photo by ${artwork.artist}`}
                /*set w-[250px] to a variable that updates for desktop + mobile*/
                className="space-y-3 h-[375px]"
                // className="aspect-[3/4] h-fit w-fit object-cover"
                width={300}
                height={400}
              />
            </div>
            <figcaption className="pt-2 text-xs text-muted-foreground">
              Photo by{" "}
              <span className="font-semibold text-foreground">
                {artwork.artist}
              </span>
            </figcaption>
          </figure>
        ))}
        {tweets.map((tweet) => (
          <SocialMediaPost key={tweet.content} {...tweet} />
        ))}
      </div>
      <ScrollBar orientation="horizontal"/>
    </ScrollArea>
  )
}
