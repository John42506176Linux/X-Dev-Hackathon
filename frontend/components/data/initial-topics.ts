// @ts-nocheck
// export interface Topic {
//   title: string
//   numberOfPosts: number
//   link: string
// }
import {Tweet, tweets} from '@/components/data/posts'
export interface Topic {
  representation: string
  top_image: string
  top_tweets: Tweet[]
}

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

// {
//   "data": [
//   {
//     "representation": "AI Optimization",
//     "top_image": [
//       "https://pbs.twimg.com/media/GLp6-LoaYAAww8H.jpg"
//     ],
//     "top_tweets": [
//       [
//         "@WilliamsburgAD @The_MJHines2 Only in Playoffs, thats why I am like, I didn’t know Lebron played for the Lakers",
//         {
//           "created_at": "2010-07-08T22:11:19.000Z",
//           "id": "164442064",
//           "name": "Brad  Knoop",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1491265240155238402/6XsgKvvP_normal.jpg",
//           "username": "CoachKnoop"
//         }
//       ],
//       [
//         "@LAbound2 This team is not discipline = 9 losses straight",
//         {
//           "created_at": "2011-12-11T16:26:54.000Z",
//           "id": "434247899",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1722232526067130368/Fp2MBJZl_normal.jpg",
//           "name": "Ray",
//           "username": "RayBbBbBbB"
//         }
//       ],
//       [
//         "@defender_ja @jordankobewade7 Funny thing is, LeBron's not even close to competing for a chip right now. 🤣 I shouldn't laugh because I'm a Lakers fan but clowns like you make it impossible not to. MJ could've been soft and joined the Lakers for 2 easy rings, but no, he chose to play for a God awful team.",
//         {
//           "id": "274183378",
//           "name": "Nick Allen",
//           "username": "nickallen824",
//           "created_at": "2011-03-29T22:07:27.000Z",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1677326082133966853/9yUkTAMp_normal.jpg"
//         }
//       ]
//     ]
//   },
//   {
//     "representation": "AI Hardware",
//     "top_image": [
//       "https://pbs.twimg.com/media/GLqAN0aWcAA4gIJ.jpg"
//     ],
//     "top_tweets": [
//       [
//         "Y'all were right. I was wrong. Skip clearly said the series was a gimme for the Lakers so that he then could hammer Lebron when it inevitably wasn't. I again failed to grasp the full extent of his chuckleheadedness.",
//         {
//           "username": "NikolaNuggets",
//           "name": "NikolaNuggets",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1709859587623673856/56SXYyXA_normal.jpg",
//           "created_at": "2021-09-19T07:07:01.000Z",
//           "id": "1439486043170885634"
//         }
//       ],
//       [
//         "No surprises there 😑 but they still got beat down 😤",
//         {
//           "created_at": "2013-10-22T17:24:41.000Z",
//           "username": "__Songz90",
//           "name": "Kratos",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1749505289433272321/-G9zf79i_normal.jpg",
//           "id": "2148695626"
//         }
//       ],
//       [
//         "oh man they are HEATED.",
//         {
//           "id": "1626542103860858880",
//           "username": "Justinvazquez__",
//           "created_at": "2023-02-17T11:20:46.000Z",
//           "name": "J🦈",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1750306286980177920/F6G4tyUW_normal.jpg"
//         }
//       ]
//     ]
//   },
//   {
//     "representation": "NFL Contracts",
//     "top_image": [
//       "https://pbs.twimg.com/media/GLrp42IaUAANR9T.jpg"
//     ],
//     "top_tweets": [
//       [
//         "Why does he always do this",
//         {
//           "id": "1741048257042599936",
//           "created_at": "2023-12-30T10:47:14.000Z",
//           "username": "NoLimitZN_",
//           "name": "No limit",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1741048581388161024/TxslRNnY_normal.jpg"
//         }
//       ],
//       [
//         "This is fucking hilarious",
//         {
//           "name": "Leel",
//           "username": "wrightkhalil1",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1508690592204738561/Gv_gJ53O_normal.jpg",
//           "created_at": "2015-10-24T07:36:24.000Z",
//           "id": "4000012873"
//         }
//       ],
//       [
//         "That was the game Momentum never regained",
//         {
//           "id": "815787066210549760",
//           "name": "BIG ISAAC",
//           "username": "BIG__ISAAC",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1690195369278271488/u6CmcTzA_normal.jpg",
//           "created_at": "2017-01-02T05:09:28.000Z"
//         }
//       ]
//     ]
//   },
//   {
//     "representation": "Performance Testing",
//     "top_image": [
//       "https://pbs.twimg.com/media/GLroeO-bkAAUpOw.jpg"
//     ],
//     "top_tweets": [
//       [
//         "RT @TactBets: IF WE WIN THIS SPORTS BET, I WILL GIVEAWAY:💸 $250 TOTAL 25 PEOPLE WHO... ($10 x 25 Stake Depo's) - RETWEET THIS POST🔁 &amp; LIKE…",
//         {
//           "id": "1778824751709872130",
//           "username": "paulgam0x",
//           "created_at": "2024-04-12T16:37:26.000Z",
//           "name": "Rhonda",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1779141964098613248/CynUojDu_normal.jpg"
//         }
//       ],
//       [
//         "RT @TactBets: IF WE WIN THIS SPORTS BET, I WILL GIVEAWAY:💸 $250 TOTAL 25 PEOPLE WHO... ($10 x 25 Stake Depo's) - RETWEET THIS POST🔁 &amp; LIKE…",
//         {
//           "id": "1716367845901410304",
//           "created_at": "2023-10-23T08:16:09.000Z",
//           "username": "teentabarwala",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1746198643865255936/dDpg4r5E_normal.jpg",
//           "name": "teentabarwala"
//         }
//       ],
//       [
//         "RT @TactBets: IF WE WIN THIS SPORTS BET, I WILL GIVEAWAY:💸 $250 TOTAL 25 PEOPLE WHO... ($10 x 25 Stake Depo's) - RETWEET THIS POST🔁 &amp; LIKE…",
//         {
//           "id": "839639275",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/549569644952948736/nnNQyktx_normal.jpeg",
//           "name": "Dreamer",
//           "created_at": "2012-09-22T12:06:44.000Z",
//           "username": "verdasco7"
//         }
//       ]
//     ]
//   },
//   {
//     "representation": "_AI Paradigms",
//     "top_image": [
//       "https://pbs.twimg.com/media/GLrych1b0AAz9Xg.jpg"
//     ],
//     "top_tweets": [
//       [
//         "@Nixxn1 @statmuse Lakers getting more Calls than every other Team= Common Ball Knowledge",
//         {
//           "id": "1224776177732280322",
//           "name": "Luka Dukic",
//           "profile_image_url": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
//           "username": "LukaDukic4",
//           "created_at": "2020-02-04T19:26:32.000Z"
//         }
//       ],
//       [
//         "As I see it; this is the most likely. My Prediction was and still is a Lakers in 5/6 only that I really wanted a Game 1 &amp; 2 in Denver; would have solidified our confidence heading back home. Let's see how Monday goes; it's very key that we win a game on the road.",
//         {
//           "id": "489453150",
//           "created_at": "2012-02-11T15:03:32.000Z",
//           "username": "ClivesGrace",
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1771610964783230976/V1TqtdHg_normal.jpg",
//           "name": "♠️"
//         }
//       ],
//       [
//         "@MagicJohnson The real mvp was the tv director of @ABC missing a play 3 minutes in to the game. Fire that incompetent.",
//         {
//           "profile_image_url": "https://pbs.twimg.com/profile_images/1694444149007585280/OD4cpzCi_normal.png",
//           "username": "Alber1512681",
//           "id": "1694444064844763137",
//           "name": "Alber",
//           "created_at": "2023-08-23T20:19:00.000Z"
//         }
//       ]
//     ]
//   }
// ]
// }
