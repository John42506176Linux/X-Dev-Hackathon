'use client'

import React, {useEffect, useState} from 'react'
import {animated, useTransition} from '@react-spring/web'
import shuffle from "lodash.shuffle"
import Image from "next/image"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardDescription, CardHeader, CardTitle,} from "@/components/ui/card"
import {ScrollArea, ScrollBar} from '@/components/ui/scroll-area'
import TwitterPost from '@/components/twitter-post'
import {Tweet, tweets} from '@/components/data/posts'
import axios from 'axios';
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
    console.log()
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

// @ts-ignore
export function List(userID) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rows, set] = useState(topics)

  useEffect(() => {
    const fetchData = async () => {
      // ... (Change the fetch part with Axios)
      try {
        const response = await axios.get('http://127.0.0.1:8000/initial_topics/3293358400');
        setData(response.data); // Axios automatically parses JSON
        console.log(response.data);
      } catch (err) {
        // Axios provides more specific error info
        // @ts-ignore
        setError(err.message);
        console.log(err.message);
      } finally {
        setLoading(false);
        console.log(data);
      }
    };

    fetchData();
  }, []);
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
  return <List userID={3293358400}/>

}
