import React from "react";

export default class TwitterPost extends React.Component<({
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
