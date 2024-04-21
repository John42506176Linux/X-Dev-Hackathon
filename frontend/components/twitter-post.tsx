import React from "react";

export default class TwitterPost extends React.Component<({
   created_at: any
   id: any
   name: any
   profile_image_url: any
   username: any
    content: any
})> {
  render() {
    let {created_at,
      id,
      name,
      profile_image_url,
      username,
      content
    } = this.props;
    return (
      <div key={id} className="flex min-h-40 place-items-center border border-gray-200 p-4 rounded-lg mb-5">
        <img
          src={profile_image_url}
          alt={`${username}'s profile pic`}
          className="w-12 h-12 rounded-full mr-4"
        />
        <div className="flex-1">
          <div className="flex items-center">
            <a href="" className="font-bold mr-2">{name}</a>
            <a href="" className="text-gray-500">@{username}</a>
          </div>
          <p className="max-w-sm place-content-center text-wrap mb-2 mt-2">{content}</p>
          <span className="text-gray-500 text-sm">{created_at}</span>
        </div>
      </div>
    );
  }
}
