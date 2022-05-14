# space-bar
The best space game in 2022.

How to play:

If you don't have Adobe AIR installed on your computer, use the file AdobeAIR.exe from this repository before launching the game.
Then, launch the Core.exe from the Core, in order to start the game.
If this is your first time playing, the game will automatically set up everything for you.

**Next, enjoy this adventure, discover new characters, learn how to operate a space ship and how to travel in this vast, open-world, space environment.
Find out what's going on, what mysteries are there hidden, and solve them.**

--



About the development:

The game was made using 4 different technologies.

• The Bar and the Travel Environment were made in Adobe Animate, using AS3, an ECMAScript dialect.

• Another locations in space (things such as the space radio or the final location) were made in Python using PyGame.

• The cinematic for the credits was made in Java, using Swing.

• All these run in different windows and have to be synchronized, and that's what the Core, done in C++, does.

We purposely made each different feature in a new technology, to somehow mimic the diversity of the space and the new planets by using diverse frameworks.




Other cool features:

• Except for some space background photos, ALL the graphic features and animations were hand-drawn by one of the team members.

• The flow of time is a very important feature through the game. For example, when getting close to a black hole, due to relativity, time flows 30x times faster. It had to be synchronized across all locations, and we successfully did that.

• No game engine was used for the bar or the travelling environment. Everything was programmed by ourselves, line by line. For example, the vehicle movements were programmed using trigonometric equations, all calculated by hand. Even the intertia for the objects was simulated in hand-written code, using physics formulas.

• To simulate real connections, the communications when using a radio are done in the back-end with a TCP server. So, the dialogue isn't actually incorporated in the code, and you get the answers from the other side with a TCP connection.

• Beside the quest itself, you also have other fun things to do, with your phone (which is to be found in the right side, with the mouse, while outside, in space). You have Radio, with cool tracks, you can call your ship to come closer to you, you have tips for playing the game, a minigame, and even a space-themed dating app.

• By exploring the space you might find other interesting planets and space objects. However, be careful not to get lost, as the space is vast and, unless you use the GPS with a fixed reference point with a code, it might be easy to go astray.

• There were hours of work for the mechanics of the ship, we wanted it to move in that certain way on purpose. It is a tiny challenge to understand how to drive it, but it is part of the game. You have to understand the directions, fight the inertia, use the "compass". Who said spaceships are easy to manipulate? :D

• We also did the design for all the sound used, did the cuts, and the mix.


All the pictures and sounds used are under CC0 - Creative Commons.

**For more cool stories, walkthrough, and details about the development of this project, check the _Stories_ directory.** 

Notes:

• I know most people can't acces a .fla file. The person who worked on it has a paid license for Animate. Therefore, a part of the code for the bar and the travel environment was pasted as plain text in the directory **Implementation**.

• The Harman watermark is a feature from Adobe AIR. Getting a premium license and removing it would cost us over $150.

• Currently, the TCP server is also installed on the local machine. If the game is to be launched in the future, maybe we will have the resources to run a real server.
