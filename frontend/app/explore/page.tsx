'use client'

import React, {useEffect, useState} from 'react'
import {animated, useTransition} from '@react-spring/web'
import shuffle from "lodash.shuffle"
import Image from "next/image"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "@/components/ui/card"
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
  likes: number
}

export interface Topic {
  title: string
  numberOfPosts: number
  link: string
}

const tweets: Tweet[] = [
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: "$GMale",
    handle: "laptopcrust",
    content: "thinkin of my next tweet",
    timestamp: "Today at 3:32 PM",
    likes: 0
  },
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: 'Twitter',
    handle: 'Twitter',
    content: 'Happy 3rd anniversary #TBT! See how "Throwback Thursday" cemented its status as a weekly Twitter tradition:',
    timestamp: '6:26 PM - Apr 30, 2015',
    likes: 0
  },
  {
    profilePic: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    userName: "$GMale",
    handle: "laptopcrust",
    content: "thinkin of my next tweet",
    timestamp: "Today at 3:32 PM",
    likes: 0
  },
]
const works: Artwork[] = [
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
const topics: Topic[] = [
  {
      title: "Fans upset over new Jujutsu Kaisen chapter leak",
      numberOfPosts: 2044,
      link: "",
  },
  {
      title: "Yuji gets a new technique",
      numberOfPosts: 15942,
      link: "",
  },
  {
      title: "Dodgers vs. Padres has fans in shambles",
      numberOfPosts: 1942,
      link: "",
  },
]
class TwitterPost extends React.Component<({
  profilePic: string,
  userName: string,
  handle: string,
  content: any,
  timestamp: string
})> {
  render() {
    let {profilePic, userName, handle, content, timestamp} = this.props;
    return (
      <div className="flex min-h-40 place-items-center border border-gray-200 p-4 rounded-lg mb-5">
        <img
          src={profilePic}
          alt={`${userName}'s profile pic`}
          className="w-12 h-12 rounded-full mr-4"
        />
        <div className="flex-1">
          <div className="flex items-center">
            <a href="" className="font-bold mr-2">{userName}</a>
            <a href="" className="text-gray-500">@{handle}</a>
          </div>
          <p className="max-w-sm place-content-center text-wrap mb-2 mt-2">{content}</p>
          <span className="text-gray-500 text-sm">{timestamp}</span>
        </div>
      </div>
    );
  }
}

  // useEffect(()=> {
  //   window.addEventListener('resize', ()=> {
  //     // console.log(window.innerHeight, window.innerWidth)
  //   })
  // }, [])
  // @ts-ignore
// export function TopicBlock() {
class TopicBlock extends React.Component<({
  topic: Topic,
})> {
  render() {
    // let {profilePic, userName, handle, content, timestamp, topic} = this.props;
    let {topic} = this.props;
    return (
      <ScrollArea className="ease-in w-full whitespace-nowrap rounded-md border">
        <Card className="sm:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle>#{topic.title}</CardTitle>
            <CardDescription className="max-w-lg text-balance leading-relaxed">
              <span className="pt-2 text-xs text-muted-foreground">
                <span className="font-semibold text-foreground">{topic.numberOfPosts}</span>k posts
              </span>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex w-max space-x-4 p-4">
              {works.map((artwork) => (
                <figure key={artwork.artist} className="shrink-0">
                  <div className="overflow-hidden rounded-md">
                    <Image
                      src={artwork.art}
                      alt={`Photo by ${artwork.artist}`}
                      /*set w-[250px] to a variable that updates for desktop + mobile*/
                      className="space-y-3 h-[225px] w-[225px]"
                      width={225}
                      height={225}
                    />
                  </div>
                  <figcaption className="pt-2 text-xs text-muted-foreground">
                    Photo by{" "}<span className="font-semibold text-foreground">{artwork.artist}</span>
                  </figcaption>
                </figure>
              ))}

              {tweets.map((tweet) => (
                <>
                  <div className="shrink place-content-center">
                    <TwitterPost key={tweet.content} {...tweet} />
                  </div>
                </>
              ))}
              <div className="flex min-h-40 place-items-center p-4 rounded-lg mb-5">
                <Button className="shrink place-content-center min-h-40 place-items-center">See more</Button>
              </div>
            </div>
          </CardContent>
        </Card>
        <ScrollBar orientation="horizontal"/>
      </ScrollArea>
    );
  }
}

export function List() {
  const [rows, set] = useState(topics)
  useEffect(() => {
    const t = setInterval(() => set(shuffle), 8000)
    return () => clearInterval(t)
  }, [])

  let height = 0
  let heightCard = 400
  const transitions = useTransition(
    rows.map(topics => ({...topics, y: (height += heightCard) - heightCard})),
    {
      key: (item: any) => item.id,
      from: {height: 0, opacity: 0},
      leave: {height: 0, opacity: 0},
      // @ts-ignore
      enter: ({y, height = 500}) => ({y, height, opacity: 1}),
      // @ts-ignore
      update: ({y, height = 500}) => ({y, height}),
    }
  )

  return (
    <div className="list" style={{height}}>
      {transitions((style, item, t, index) => (
        <animated.div className="card" style={{zIndex: topics.length - index, ...style}}>
          <div className="cell">
            <TopicBlock topic={topics[index]}/>
          </div>
        </animated.div>
      ))}
    </div>
  )
}

export default function ExplorePage() {
  // const [transitions, api] = useTransition(data, () => ({
  //   from: { opacity: 0 },
  //   enter: { opacity: 1 },
  //   leave: { opacity: 1 },
  // }))
  //
  // return transitions((style, item) => (
  //   <animated.div style={style}>{item}</animated.div>
  // ))
  return <List/>

}
