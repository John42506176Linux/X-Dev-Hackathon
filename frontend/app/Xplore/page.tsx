// @ts-nocheck
'use client'

import React, {useEffect, useState} from 'react'
import {animated, useTransition} from '@react-spring/web'
import shuffle from "lodash.shuffle"
import Image from "next/image"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "@/components/ui/card"
import {ScrollArea, ScrollBar} from '@/components/ui/scroll-area'
import TwitterPost from '@/components/twitter-post'
import {Tweet} from '@/components/data/posts'

// @ts-ignore

export interface Artwork {
  artist: string
  art: string
}

export interface Topic {
  title: string
  numberOfPosts: number
  link: string
}

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

export interface Topic {
  representation: string
  top_image: string
  top_tweets: Tweet[]
}

// export interface Tweet {
//   created_at: any
//   id: any
//   name: any
//   profile_image_url: any
//   username: any
// }

const testTopic: Topic = {
  representation: "Sample Topic",
  top_image: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
  top_tweets: [] // Empty array for top_tweets
};

const testTopics: Topic[] = [
  testTopic,
  testTopic,
  testTopic,
]

// @ts-ignore
export function List(userID) {
  const [user, setUser] = useState(null)
  const [rows, set] = useState(testTopics)
  const [topics, setTopics] = useState(testTopics)
  // @ts-ignore
  const mapJsonResponseToTopics = (data: any[]): Topic[] => {
    // @ts-ignore
    return data.map((item) => ({
      representation: item.representation,
      top_image: item.top_image[0],
      // @ts-ignore
      top_tweets: item.top_tweets.map((tweetArray) => ({
        // @ts-ignore
        created_at: tweetArray[1].created_at,
        id: tweetArray[1].id,
        name: tweetArray[1].name,
        profile_image_url: tweetArray[1].profile_image_url,
        username: tweetArray[1].username,
        content: tweetArray[0]
      }) as Tweet[]) // Fixed parentheses, added type assertion
    }));
  };

  const fetchTopics = async () => {
    console.log("Sanity Tests")
    const baseUrl = "http://localhost:8000/initial_topics/3293358400"
    try {
      const response = await fetch("http://localhost:8000/initial_topics/3293358400");

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }

      const todos = await response.json();
      setTopics(mapJsonResponseToTopics(todos.data));
      // for (let i = 0; i < ; i++) {
      //
      // }
      console.log("NEW PAGE:", todos); // Assuming todos is an array
      // setTodos(todos.data)
    } catch (error) {
      console.error("There was an error fetching todos:", error);
    }
  };

  useEffect(() => {
    const t = setInterval(() => set(shuffle), 10000)
    fetchTopics()
    return () => clearInterval(t)
  }, [setTopics,topics])

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

class TopicBlock extends React.Component<({
  topic: Topic,
})> {

  render() {
    // let {profilePic, userName, handle, content, timestamp, topic} = this.props;
    let {topic} = this.props;
    console.log("TOPIC: " + topic)
    // @ts-ignore
    // @ts-ignore
    return (
      <ScrollArea className="ease-in w-full whitespace-nowrap rounded-md border">
        <Card className="sm:col-span-2">
          <CardHeader className="pb-3">
            <CardTitle>#{topic.representation}</CardTitle>
            <CardDescription className="max-w-lg text-balance leading-relaxed">
              <span className="pt-2 text-xs text-muted-foreground">
                {/*<span className="font-semibold text-foreground">{topic.numberOfPosts}</span>k posts*/}
              </span>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex w-max space-x-4 p-4">
                <figure key={topic.top_image} className="shrink-0">
                  <div className="overflow-hidden rounded-md">
                    <Image
                      src={topic.top_image}
                      // alt={`Photo by ${artwork.artist}`}
                      /*set w-[250px] to a variable that updates for desktop + mobile*/
                      className="space-y-3 h-[225px] w-[225px]"
                      width={225}
                      height={225}
                    />
                  </div>
                  {/*<figcaption className="pt-2 text-xs text-muted-foreground">*/}
                  {/*  Photo by{" "}<span className="font-semibold text-foreground">{}</span>*/}
                  {/*</figcaption>*/}
                </figure>


              {topic.top_tweets.map((tweet) => (
                <>
                  <div className="shrink place-content-center">
                    <TwitterPost key={tweet.id} {...tweet} />
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

export default function ExplorePage() {
  return <List userID={3293358400}/>
}
