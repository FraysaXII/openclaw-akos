---
source: /Users/fay/cd/projects/nfq/ue-quickwins/supporting_docs/recordings/27-02-2026 15.11 shadow gpu x holistika meeting.mp3
source_type: .mp3
converted_at: 2026-03-03T15:54:21
title: "27-02-2026 15.11 shadow gpu x holistika meeting"
---

_Audio transcription — Duration: 01:00:24 — Language: en — Speakers: 3_

## Chapters

### Faisal: Julian will accompany me on this call (00:03 — 00:29)
_Q4 2017_

Faisal: I'll just quickly introduce Julian to you. He's basically my manager, so he's going to accompany me on this call. He has a deeper knowledge of the needs you'll have and how we can hopefully answer to them.

### Christophe is building a consultancy focused on GPUs (00:29 — 04:19)
_Holistica Research: The Future of GPUs_

Right now I'm building a consultancy. Before, it was a research group in which we were tracking several news for different markets. What we want from Shadow is to have an infrastructure of GPU specifically. We focus on consultancies, plain and simple.

### You mentioned DeepSeq, you talked about the size of the model (04:23 — 06:41)
_Microsoft Cloud: GPUs in the cloud_

We indeed provide some solutions when it comes to having access to GPUs in the cloud. We tend to avoid vendor locking, and that is the primary reason. We won't stick to one, we prefer to do both and everything.

### Use of DeepSig is primarily for inference, not training (06:41 — 07:28)
_Is DeepSig useful for inference?_

Is it rather for inference use case, or is it rather fine-tuning, or even maybe training? No, not today. It's only inference because training already, because of the way the context has grown so much, it's not worth it.

### We have solutions for both, uh, type of usage you're talking about (07:29 — 17:18)
_OpenStack vs. Kubernetes: How to Host a_

We have two ways of working primarily with, uh, with, with our providers is, is API calling directly. The second solution is not yet in production, but we have a partner that provides the opportunity to give this layer of service where a serverless approach could be feasible. The best way maybe would be to open you an OpenStack project to see if the model can be hosted.

### We have different ways for you to get access to the infrastructure (17:18 — 19:52)
_Guarantee vs. Spot: Is IT Infrastructure Secure?_

We have different ways for you to get access to the infrastructure. We have the guaranteed one, where you have access 24/7 for a whole month. We also have another solution which is spot, which is basically a pay-as-you-go approach. If this goes well, then we will build a SaaS at the end of the day.

### When it comes to the prices, we have dedicated website where we have some information (19:53 — 24:28)
_Kirve 2.8 and 3.8: Minimum-_

The A4500 is €250 per month for one GPU. With a minimum volume of hours of usage, the hourly price is 35 cents per GPU per hour. If what we are doing here works, we can provide to others access to applications, go inside and help them do SaaS like we do.

### There is a possibility to provide the serverless approach with us and our partner (24:29 — 26:43)
_OpenStack Serverless and API Endpoints_

We want to create a monolithic GitHub repo in which we will control all of our operations. There is indeed a possibility, uh, to provide the serverless approach with us and our partner providing the endpoints. I think that making things simple at the beginning would be the fastest way to proceed.

### Groq and Vercel AI multiply the speed of the inference (26:44 — 27:56)
_Inferring with DeepSeq on Cloudflare_

We have Groq with Q, we have Vercel AI, These are the main— we have Cloudflare also. About inference, I mean, I say today DeepSeq, but if I don't have it, okay. Those are the ones that we call.

### Okay, I need also to, to get some visibility of the potential volume (27:58 — 29:14)
_What is the potential for business-to-consumer deployments of Post_

It depends on how experimental this proof of concept will go and who is the buyer. If we find the use case in which the model is profitable enough to do a business-to-consumer, then the numbers should grow a lot. But at the beginning, we'll be best to go until we know exactly.

### When it comes to the data center, would you have a preference (29:14 — 36:04)
_OVH Data Center_

When it comes When it comes to the data center, would you have a preference? I believe European markets? Next step would be serverless. Do you have other Topics, other questions?

### Faisal: It's about providing infrastructure in an escalable way (36:04 — 40:03)
_Open Cloud 2.8: Autonomous Replication_

The next step would be actually to have this autoscaler and what comes around. Not yet, but maybe it's a good timing in the end. Depending on the test, we could start with either the guaranteed and/or the spots. Thanks a lot for your time, Faisal.


## Transcript

**[00:03] Speaker A:** Hello and sorry for the delay.

**[00:06] Speaker B:** Hello again, Faisal.

**[00:09] Speaker A:** Nice to meet you.

**[00:09] Speaker C:** Nice to meet you too.

**[00:10] Speaker A:** Here, thank you for your time.

**[00:13] Speaker B:** Yeah, thanks as well for your time. Uh, so I'll just quickly introduce Julian to you. He's basically my manager, so he's going to accompany me on this call. Uh, he has a, let's say, a deeper knowledge of the needs you'll have and how we can hopefully answer to them. So I suggest maybe you can quickly introduce yourself, uh, what you're doing, and it's especially what you're trying to get out of Shadow in terms of GPUs.

**[00:39] Speaker A:** Okay, so the— right now I'm building a consultancy. Before, it was a research group in which we were tracking several news for different markets. The reason is I am a project manager I was working at IBM, so that was more from a business analyst to data scientist, but more in the project-based services they have. Sorry, because the camera, I don't know what it's doing, but this is like automated video, so I think I'm bugging in the camera.

**[01:13] Speaker B:** It's fine as long as you can hear what you're saying.

**[01:16] Speaker A:** Okay, thanks. So the thing is that I, I stuck on the idea of having this management system like I was taught in IBM. So that's what I am doing in my side jobs. I do projects, I help others doing strategy projects, finance projects, marketing, maybe startups, or even sometimes only research about what's going on. Like for example, in the COVID we were investigating about what was later happened in Ukraine. We even have an ONG there back in 2018, and this was a lot of data of a lot of ways of classifying that. And that is where Holistica Research comes in as a solution that I'm deploying to— and it's a corporate intelligence agency at the end of the day, so because we need money in any way We do two things. So we focus on consultancies, plain and simple, data, finance, marketing, operations, or people, tech also. But because tech is so big, especially today, and that was what we researched, that it would explode, but we didn't know when, we separated tech always. So this is why before I wasn't speaking about tech at all at the beginning, because this whole is separate. So in tech, we built a lot of use cases in real time between GPT-3.5 up until today, in which we have agentic frameworks on 2023 on GitHub running with LLM as operating services in Scalidraw already back there. And so this was the research directly there. We didn't publish because we didn't want to get cut off in the later deprecating methodologies that you build back then. And this is why today what we want from Shadow is to have an infrastructure of GPU specifically in which we could still research, build something, know what's happening. Like, for example, CloudBot was the example that I gave Jean-Jacques the other day. CloudBot was exploding. We know, we knew that a lot. Since Oyama was there, we have prototyped a lot of things. But when we go now to there with our DeepSeq R1, we can only go with 14 billion parameters instead of 70, because that 70 would be 24 to 32 gigabytes of RAM of a GPU, and that is like something on demand normally in those cases. So having our repo pointing to an API which, uh, similar to Rumpod would be. We are working this in this way. So if you work something like that, I understand that OpEx stack more or less work like that. We could work together, I think.

**[04:16] Speaker C:** Okay, quite clear.

**[04:18] Speaker A:** Thanks a lot, Christophe. Thank you.

**[04:23] Speaker C:** Um, we indeed provide some solutions when it comes to having access to GPUs in the cloud. You mentioned DeepSeq, you talked about the size of the model. So as of today, you work with the 12?

**[04:40] Speaker A:** 14.

**[04:41] Speaker B:** 14?

**[04:42] Speaker A:** Yeah.

**[04:42] Speaker C:** And you would like to have a solution to have the 70 billion model works? Okay. And as of today, you are using RunPod? And you are looking for an alternative solution for which reason? Is it like pricing? Is it sovereignty? Is it something else?

**[05:06] Speaker A:** We tend to, you know, this is something that we wrote in our documentation to our customers, we tend to avoid vendor locking, and that is the primary reason. Not only for us, because we build things that other people, we speak with them and they may want this solution for another things. And so this is why we, we want to build things in the same thing. For example, Google and Azure, we have both. We have AWS doing the same structure, at least to test it works. So maybe we will work here, we will maybe call Rumpod, but it's, this is maybe is We won't stick to one, we prefer to do both and everything. But at first we need of course to do something first, and that is where ChatGPT comes in front of Groompot. Because it's true that they have templates that help inside, so you call the API, but behind they have maybe some code with some templates like Stable Diffusion or some things that maybe help us. That was the main goal. And because you— I didn't know if you did that before, but now with the templates everywhere, so I prefer to have a real PC like I have with our PC today. And then especially if it is the same provider with GPU, then for me, for us, it's like that was the perfect solution. That is mainly why we are here also.

**[06:40] Speaker C:** Okay. And regarding the type of usage you make with DeepSig, is it rather for inference use case, or is it rather fine-tuning, or even maybe training?

**[07:01] Speaker A:** No, not today. It's true that when we started in the room posting, I was saying before it was training. And that was the template came in. So this is one of the use cases that is the commission right now.

**[07:15] Speaker C:** And sorry, right now?

**[07:17] Speaker A:** It's the commission. In this case, we don't do that anymore. So it's only inference. It's only inference because training already, because of the way the context has grown so much, it's not worth it. Okay.

**[07:31] Speaker C:** Okay, quite clear. Thanks for sharing the details. Basically, uh, we, uh, have this new solution because I, I believe you know Shadow PC with the, the SaaS service with a virtual machine with Windows installed on it that runs on server with high-powered GPU and CPU and RAM. And we have launched a new a new type of offer, which is basically a pass offer where the customers could directly get access to the infrastructure. The technology we use for that is OpenStack, which is a, a solution aiming at preparing the instance the way the end user needs it, meaning that you can select the flavor, the number of GPU you would require within an instance. Etc., etc. Are you familiar with OpenStack a little bit?

**[08:31] Speaker A:** I, I saw it since Sergio told me. I was interested in some similar solutions also, like this Nix also infrastructure, like everything that is one infrastructure for everyone. Okay. And that is something that I'm, I'm kind of familiar at least with the logic.

**[08:52] Speaker C:** Okay, so yeah, I, I, I could understand what, uh, in terms of, uh, handling the instances with your flow, would you work with API or Kubernetes, or which would be the technical solution you plan to, to use?

**[09:12] Speaker A:** Well, for us it's, uh, it's okay, uh, it will be more— well, if you have serverless or something similar to serverless, that would be excellent. Okay, because, uh, um, today we have two ways of working primarily with, uh, with, with our providers is, is API calling directly. I will show you, if you allow me, uh, our ERP so you can see more or less our UI and how we build things for ourselves, one of those use cases. And, and, and then this would be API. So we build our thinking in our house, we build our UI, it is calling there, and we have our front end calling directly your API and calling our database. So that is the primary use case, especially from, from POC. And, and then when that is done, it's like if you have a serverless solution, that would be something like Okay, what is your GitHub repo? And that way you can synchronize even better, but that would be only nice to have.

**[10:20] Speaker C:** Okay, uh, okay, we have solutions for both, uh, type of usage you're talking about. Historically, uh, OpenStack is the first step to, let's say, uh, prepare the instance the way you need it to be, and then you can have access to it either by API who is calling it or Kubernetes should you have a pod already existing and that you directly plug into our own Kubernetes. And the second solution is not yet in production. We're rather investigating this area, but we have a partner we work with that provides us the opportunity to give this layer of service where a serverless approach could be feasible. But it's quite new. We have less historic, so maybe it may take some time. And when it comes to the first solution, we propose different type of GPUs. The highest configuration embarks 20 gigs of VRAM for a single GPU. So there is this question of should you need more VRAM, we are able to provide instances that are up to 4 or even 8 GPUs, which theoretically could go up to 1 160 gigs of VRAM. But of course, it's theory. In real life, there might be a drop of performance. But if your goal is to host the 70 billion parameters model from DeepSeq, we could try something. I think the best way maybe would be to open you an OpenStack project so that you can directly try yourself to see if the model can be hosted. We could try with the A40— A4500 GPU, which is the one with 20 gigs of VRAM. For instance, to start with, we could upload an instance with 4 GPUs I believe that might be a good way to start to see how this works, whether you can host the model and whether it performs properly. Um, firstly, what do you think of this proposal? Would it make sense?

**[13:01] Speaker A:** It makes sense, and thank you very much, because that way I can try it and, and see, uh, for myself and everything. So it's, uh, 24 GB to 32. The estimate that we have for such a model. I'm glad that you say that you have even more because there was a— which one was— there was a model that they did before, they weren't so efficient, that took 128 GB. It was an experimental one, and the medical ones also especially, they are really, really heavy. So this is good. We are not touching it, but it's good to know because it can happen. And vision also, I'm not touching vision at the moment. We have researchers, we have even customers asking for that, to go into the vision and game models, especially the Chinese one, the ones from Huion, the ones from Tencent. I don't know if you know the company, it's the one who, that holds Epic Games, Ubisoft, they have everything, Riot Games. And that one, they are launching models, 3D in this case. So it's literally doing— I did a simulation, it did a, um, it did like a toy of Luffy from One Piece, literally from an image from the manga, and it was 3D. You can even rotate it and put it in Blender. Okay, so that's for the other use case, as you said.

**[14:32] Speaker C:** It's a video GenAI, basically.

**[14:34] Speaker A:** It's a 3D GenAI. They have also the same ones, they also have the version video.

**[14:40] Speaker C:** Okay, okay. Uh, the render part and the performance linked to rendering is quite good on our GPUs. Basically, it's, uh, it's those GPUs that make the virtual machines run, uh, where we have a lot players, gaming players that take benefit from it. And as a consequence, it was an absolute prerequisite on our side to have GPUs that are good into processing, rendering, and 3D and so on. So I believe the performance when it comes to 3D GenAI inference would be great. The key question would be the capacity to host the 7 billion parameters model? So the test will answer this question. Um, do you have any requirements in terms of storage?

**[15:34] Speaker A:** Storage, um, it should be— yeah, it's a good question. Um, I mean, we could go for, I think, 1 tera, or at least should be the case. Well, maybe we can go for half, at least for the test. I don't know how much it— let me see, maybe I can look at it. How much it—

**[16:02] Speaker C:** by default, we provide for the test 200 gigs storage. That's the question, because if you need more due to the models or due to the data transfer and so on, Might be better to know.

**[16:16] Speaker A:** Yeah, because these guys sometimes they do half a tera, sometimes they— okay, well, some people say it could be even 48GB VRAM. It's not— it's difficult to say because it depends on a lot of— yeah, and about storage or I could go to Hugging Face, but I think it's faster here. No, it's okay, it's okay. It can be, uh, they say it's about 100 to 150 days of storage. So I will check it out. But yeah, the 200 would be okay in the end, then, then that's okay, that's okay for, for the last. It's perfect.

**[17:16] Speaker C:** Okay, uh, okay. And there is also another question regarding the type of usage, meaning that the— we have different ways for you to, uh, to get access to the infrastructure. We have what we call the guaranteed one, where you are— you have access 24/7 for a whole month to an instance that can be up and running through the month without being stopped, which allows, for instance, really good performance for real-time use cases. Or should you need to avoid cold starts, or should you need a lot of reactivity, this is a solution that works really well. And also there is the benefit that since you're the only one to have access to it, when you, when you start a task, the task is performed once it's over, meaning that there is absolutely no case where the machine would stop, where the instance would stop, and why you would lose the job. That's the guaranteed approach, uh, and it's for whole months, and it's billed, uh, for instance, once a time, no matter the usage you have. We also have another solution which is spot, which is basically a pay-as-you-go approach. It's on an hourly rate. You get access to an instance if there is one available in the data center you will be located at. And the thing with Spot is that we can take back the instance should we need it. Example, for the VDI, for the virtual machine users, I think that Jean-Jacques already shared with you the fact that we have a 15-minute window where you can save the jobs that are incoming. Basically, is there a preferred way on your side when it comes to conception, or that there is none?

**[19:27] Speaker A:** Well, for now, uh, we, we have to choose scenarios. So for now, we don't mind cold starts. Um, we can go with that, but because we are doing inference from models in which we are already are in, in, you know, research scenario. But if this goes well, then we will build a SaaS at the end of the day. So this is also one of the reasons I wanted to speak with you, because when I go to the web page, you have both. But I wanted to, to speak up with you about this transition, um, how it goes, and also know about the prices a little bit more of this special case that we're talking about, because we will do both at the end of the day. I think when we go for SaaS, we have a database, and that database is expected to be 24/7.

**[20:17] Speaker C:** Okay, uh, okay. When it comes to the prices, we have a dedicated website where we have some information. Basically, the key numbers that you should have in mind, uh, the guaranteed, uh, model where where you have 24/7 access, for the A4500 is €250 per month for one GPU, meaning that if you need an instance that requires 4 GPUs, it's 4 times the price. When it comes to data transfer, there is no bill, so there is no extra cost, meaning that no matter how how much data you use. There is no egress fees, there is no ingress fees, no extra cost. You, you have a budget under control directly based on the GPUs you have subscribed to. When it comes to spot, the hourly price for the A4500 is 35 cents per GPU per hour. With a minimum volume of hours of usage. If this minimum is not reached, the price might be a little bit higher, around 40 cents to 45 cents. But basically, yeah, it's really, really less expensive due to the fact that it's a really pay-as-you-go product. And this fits the situation where you don't need a 24/7 instance but just from time to time during business hours inference, like 6 to 10 hours a day. That would be a good model because it's, uh, it's not an obligation for you to have it up and running all the time.

**[22:12] Speaker A:** We go for that one, I think, because for us and for the customers that we touch, and then we expect Hopefully when they come to you with them, it would be probably this last one option, this pay-as-you-go, because we are never sure how many users one is going to have. And then when one is sure, not every— when you go to production, or in our case, for example, one use case that we are going to do is if what we are doing here works, we can provide to others access to applications, go inside and help them do SaaS like we do. So this is an example, for example, if I may share. I know we may be a little bit off schedule, but this is our SaaS, more or less. So we build it only for us just to put our things This is, this is the application that we expect. Madeira is an orchestrator, the first one that we did on 2023. Kirve is an application that is able to gather data from several sources, no matter if it is YouTube, if it is video, it is Jira, whatever. So this kind of things, they, they will have their documentation at the end of the day. So this documentation, well, it's, I think it would be, well, let's see if it works, but this documentation is, I open it, sorry, in another tab, it will be the basis for you to go to another person and say, okay, if you want to provide Kiribati to another person, you can go through us, you can, We will build for you, we will use the GPU for the models behind that only you and us know what it is. And we will have two models. We will do direct consulting or we will explain like this, train people to do this and help them build that for their companies or outside. So we are consultants for other consultants too.

**[24:29] Speaker C:** And when I, I see the API endpoints regarding the serverless approach, the, the targets that you would look for is basically providing an endpoint to your customer that would run on, on, on the specific infrastructure that would make the model runs. Is that basically what you, you would like to do?

**[24:55] Speaker A:** That's exactly it. If we manage to do that, first we do run POCs, right, to be sure, to be right. But this year we are already mature, we think, with our ideas to continue to grow. And in that scenario, the serverless case is really, really nice for us because we want to create a monolithic GitHub repo in which we will control all of our operations. We will be consumers of of that one, of those endpoints also. So that way we, for example, the thing that I showed you could be separated, could be out of this structure, uh, reading from our main infra which is running, uh, with Shadow behind.

**[25:37] Speaker C:** Okay, okay, that's interesting. That might be another opportunity to, to discuss, uh, once you have tested the OpenStack, because As I mentioned, we have a partner that allows us to provide a serverless solution that we do not yet have the service internally, so that could make sense. Thing is, I believe it might be better to start with the, the test with OpenStack so that you from the beginning are sure that the models are up and running properly. Otherwise, it won't be necessary to then move to the next phase where we would have our partner, uh, into the discussion. I, I think that making things simple at the beginning would be the fastest way to proceed. But there is indeed a possibility, uh, to provide the serverless approach with us and our partner providing the endpoints, uh, with a specific model hosting at the end of the flow. Um, okay, okay, that should, that should do.

**[26:44] Speaker A:** May I ask, uh, well, if you speak with your partner or internally, or you, um, two things about that is, uh, when you do this, the infrastructure that you have behind, uh, we have Groq, we have, for example, Vercel AI, which are integrating different use cases from others. So this one I know, but I don't know how, but I know that they multiply the speed of the inference. So it's not rather like aggregating APIs of them, but this one, the people have built a logic on top of that to accelerate the inference itself. So in that cases, we have Groq with Q, we have Vercel AI, These are the main— we have Cloudflare also. So these are our 3 providers today. About inference, I mean, I say today DeepSeq, but if I don't have it, okay, I want to call people who have DeepSeq, and those are the providers. Those are the ones that we call, and then they distribute, they do whatever, and they, yeah, they answer.

**[27:54] Speaker C:** Okay, okay, clear. Interesting. Okay, I need also to, to get some visibility of the potential volume because there will be a question of capacity availability into our data centers. Do you have in mind even the rough estimate of the volumes that you would require?

**[28:18] Speaker A:** Or I cannot say for sure because it depends on how experimental this proof of concept will go and who is the buyer. Because if it is really experimental, then we will focus on monolithic and developer experience. But if we find the use case in which the model is profitable enough to do a business-to-consumer, then the numbers should grow a lot. We are ready for everything. Our database is Postgres and we are We have a capability of several million users today with, uh, with, uh, I mean, the auth schema, everything. People can log in different things. So this is already set up, so we are ready for that. But at the beginning, we'll be best to go until we know exactly. So yeah, that's more or less what I can say.

**[29:13] Speaker C:** Okay. And when it comes When it comes to the data center, would you have a preference? I believe European markets?

**[29:21] Speaker A:** Thank you, thank you. It's a really good question that I still have because they changed it last year. My question, it was Ohio, US East 1 always. But today, because Trump, France is my preference today. And also because France is more restrictive than the rest of European Union. So I mean, it's France because at least if, if we have an issue in Europe, it will stay on France, which is the regulation of France also.

**[30:00] Speaker C:** Yeah, exactly.

**[30:01] Speaker A:** That's why. That's why.

**[30:02] Speaker C:** So better France. We have 2 DC in France, so We have some, uh, we have some, some options there. Just for you, for your information, should it be a topic in the future, we also have one in Germany, Frankfurt. We have two in the US, one in Washington, DC, one in Portland. So it's basically West and East Coast. And also, should you have business opportunities in Canada, we also Laval and Montreal. And we are physically located within OVH data centers, so it's a high standard quality security backed, and also performance when it comes to bandwidth and everything. So I, I figured it was important for you to know, just to have the information and the global overview of the Solution. Uh, okay.

**[31:01] Speaker A:** And also, I'm sorry to interrupt, but also I forgot before, another reason is also because I'm based in Madrid, so the marketing offline will be probably here and people want to have the data center also close. So France is also good for that.

**[31:17] Speaker C:** Okay, okay, okay, okay, okay. Uh, that's, that's good. We have, we have two actually in France, two DCs, so I believe we'll find a solution. Okay, what else do we see? Now I have the DC, I have the instance, we can try open stack. Next step would be serverless. Yeah, what we can do, if that's okay for you, we circle back internally to have to start implementing the trial. You, you would have a set of hours for you to test the solution, see whether the instance performs the way you would like it to be. We will put 4 GPUs, or at least we will inform internally that you would need 4 GPUs within the same instance to have the test up and running. It's vacations, or at least bank holidays in France right now. So we have people coming, we are— we have people getting back, etc. So it won't be, uh, by the, the beginning of next week, but I believe in the, in the coming days we will reach back to you. Um, and maybe the next step would be, uh, yeah, to provide you the credentials to get access to the instance, and then we circle back should you have any questions. We have some people that might be interested in accompanying you. We have our lead product that is currently on vacation actually, so that was not the best timing, but Maybe end of next week. Should you have other questions, especially regarding the serverless approach, he would be a good point of contact since he's working on the product, serverless and everything. So he might be interested in your insights and specific needs. And also, if you have some troubles managing the instance with OpenStack and whatever We have engineers as well that can help, so really don't hesitate should you have any questions. So also we can plan a 15-20 minute call in order to debug whatever would happen.

**[33:46] Speaker A:** Very nice, really nice of you. Thank you very much.

**[33:49] Speaker C:** Okay, sounds great. Uh, I have all the relevant information to start on my side. Do you have other Topics, other questions?

**[34:00] Speaker A:** Uh, I think I covered most, and if not, you, you already, already said it was the inference, the main, uh, question. I mean, uh, miscellaneous question that I had. I think the rest is clear. Yeah, everything, everything's clear.

**[34:17] Speaker C:** And actually, I'm just thinking about one thing. Did you have the chance to go on our website with the GPU cloud offers?

**[34:26] Speaker A:** Well, that was where I, I signed.

**[34:29] Speaker C:** Okay. Yeah, my bad.

**[34:31] Speaker A:** No, no, no, no, it's normal. It was, uh, it was, it was really good and you had to calculate it and everything, but then I, I started counting the days and I said, oh yeah, I think I need to speak.

**[34:42] Speaker C:** And I don't know if you notice, but if you go in the hero, the top right level, that there is a documentation, uh, button where you can have all all the technical, uh, references when it comes to managing the cluster, using the API, how OpenStack should work, etc.

**[35:04] Speaker A:** So, yes, I saw it.

**[35:05] Speaker C:** Yeah, you, you can go there to already have a, a quick look of what is technically feasible. Uh, that may save some time and some questions. But I just wanted you to know that we have this documentation that you can rely on.

**[35:22] Speaker A:** I read it. It's possible. What you offer is really nice. It's integrated in our libraries and everything. We did some tests at least with the mockups data, and everything is going fine. This is a good documentation.

**[35:41] Speaker C:** Great, great. Yeah, and again, we have engineers that are specialized to accompany and possibly find tailored solutions depending on your technical restraints. So let's keep in touch, and, uh, should there be a need, we can, uh, we can set up a quick call to solve everything that could happen.

**[36:04] Speaker A:** Okay, and just one, one last question, if I may, just, uh, it's different from that this is clear, or it's a separate thing. It's about the capability to provide infrastructure in an escalable way. Another question that I have, you know, well, you're an expert on that specifically. So if I want to build something that is a micro application that I want to scale, scale always, do you provide some kind of service like that?

**[36:36] Speaker C:** Meaning, for instance, autoscaler and replicas that pop automatically depending on the peak and everything?

**[36:42] Speaker A:** Exactly that.

**[36:43] Speaker C:** Okay, uh, not yet. It's in the roadmap, but that is typically the kind of topics that Lucas, the product lead, would be interested to further investigate because he has already this feature in his list. If it's the possibility to enlighten the need and to further investigate what would you operate rationally, that would be a good opportunity for him to really have the best solution for you.

**[37:19] Speaker A:** Okay, we can speak together, but if you want to give him a spoiler, it's about sandboxing for agents because maybe he's investigating because of that, because that part is really hot because Open Cloud use case that brought me to you is because we are doing social media for our own ages. So they already had what I showed you before, but now they can collaborate with others that have that, and each of them has a sandbox. Even if you come, all of us come, these users is multiplying every sandbox of the system. And they're working on the same system. So this kind of auto-replication things that we build ourselves, like this architecture, when you at least have the possibility to scale, which is really something that we cannot do— this is our hard stop. Um, we can theoretically do it for 1, 2, 3, 4, but not indefinitely.

**[38:18] Speaker C:** Okay, yeah, yeah, that's definitely something It's something we have in mind. The, the, the last feature that we shipped were basically the spot and some specificities regarding the way the offer works. But, uh, in the grand scheme, the next step would be actually to have this autoscaler and what comes around. So yeah, we plan to have it, not yet, but maybe it's a good timing in the end. And depending on the test, I'm sure you are satisfied with the performance, we could start with either the guaranteed and/or the spots. And by that time it's implemented, we can also work on our side on the autoscaler, and that would be then the solution for you to have access to that.

**[39:02] Speaker A:** So nice.

**[39:03] Speaker C:** But yeah, let's further discuss it, uh, maybe end of next week or the one after, once you have settled the test and everything, to just clarify what's it would be done.

**[39:12] Speaker A:** Perfect, let's do that.

**[39:14] Speaker C:** It's pleasure.

**[39:14] Speaker A:** Okay, cool. Thank you very much, it was really nice to speak with you.

**[39:18] Speaker C:** Yeah, it was very nice. Thanks a lot for your time, Faisal. And, uh, next step is on our side. We get back to you regarding the test credentials and everything so that you can already start. And if, if needs be, we can of course stay in touch either with email or phone call if necessary.

**[39:35] Speaker A:** Perfect. Thank you, Faisal. Thank you. Bye-bye.

**[39:39] Speaker C:** Thanks a lot.

**[39:40] Speaker A:** Bye. Crazy.


## Key Highlights

- inference use case (mentions: 1, relevance: 0.05)
- different use cases (mentions: 1, relevance: 0.05)
- use cases (mentions: 5, relevance: 0.05)
- Open Cloud use case (mentions: 1, relevance: 0.05)
- different ways (mentions: 1, relevance: 0.05)
- different things (mentions: 1, relevance: 0.05)
- instances (mentions: 2, relevance: 0.05)
- other questions (mentions: 2, relevance: 0.04)
- tailored solutions (mentions: 1, relevance: 0.04)
- OVH data centers (mentions: 1, relevance: 0.04)
- models (mentions: 7, relevance: 0.04)
- business hours inference (mentions: 1, relevance: 0.04)
- data transfer (mentions: 2, relevance: 0.04)
- real time (mentions: 1, relevance: 0.04)
- GPU (mentions: 11, relevance: 0.04)