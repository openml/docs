The purpose of this document is to formalize the governance process used by the [OpenML project](https://openml.org) (including the [OpenML organization on GitHub](https://github.com/openml) which contains all code and projects related to OpenML.org), to clarify how decisions are made and how the various elements of our community interact. This document establishes a decision-making structure that takes into account feedback from all members of the community and strives to find consensus, while avoiding any deadlocks.

The OpenML project is an independent open source project that is legally represented by the [Open Machine Learning Foundation](https://new.openml.org/about). The Open Machine Learning Foundation is a not-for-profit organization supporting, but not controlling, the OpenML project. The Foundation is open to engage with universities, companies, or anyone sharing the same goals. The OpenML project has a separate governance model described in this document.

This is a meritocratic, consensus-based community project. Anyone with an interest in the project can join the community, contribute to the project design, and participate in the decision making process. This document describes how that participation takes place and how to set about earning merit within the project community.

### Roles And Responsibilities

<img src="https://github.com/openml/docs/raw/master/docs/img/OpenML-governance.png" alt="governance" width="300"/>

#### Contributors

Contributors are community members who contribute in concrete ways to the project. Anyone can become a contributor, and contributions can take many forms, a non-exhaustive list includes:
 - making contributions to code or documentation
 - being actively involved in OpenML meetings such as monthly online calls or in-person hackathons
 - helping users on GitHub issue trackers or on other platforms (e.g., Slack)
 - help with the organization of events and/or otherwise promote OpenML
 - make contributions of other kinds recognized by other core contributors (e.g., writing about OpenML)

Contributions that make changes to the content of an OpenML repository require a pull request and have to be approved through the decision making process outlined below.

#### Core contributors
Core contributors are community members who have shown that they are dedicated to the continued development of the project through ongoing engagement with the community, for example in the ways outlined above. They have shown they can be trusted to maintain OpenML with care. Being a core contributor is represented as being an organization member on the OpenML GitHub organization, and comes with the right to cast votes in the decision making processes outlined below.

Being a core contributor allows contributors to more easily carry on with their project related activities. For example, by giving them write access to the project’s repository (abiding by the decision making process described below, e.g. merging pull requests that obey the decision making procedure described below). They may also partake in activities not accessible to regular contributors that require greater levels of trust from the community, such as conducting code reviews or posting to social media channels. The access granted should be proportionate to the contributor’s contribution history and planned contributions. 

New core contributors can be nominated by any existing core contributors. Once they have been nominated, there will be a vote in the [private OpenML core email list](https://lists.lrz.de/mailman/listinfo/openml-core) by the current core contributors. While it is expected that most votes will be unanimous, a two-thirds majority of the cast votes is enough. The vote needs to be open for at least 1 week.

Core contributors that have not contributed to the project in the past 12 months will become emeritus core contributors and recant their commit and voting rights until they become active again. The list of core contributors, active and emeritus (with dates at which they became active) is public on the OpenML website.

#### Steering Committee

The Steering Committee (SC) members are core contributors who have additional responsibilities to ensure the smooth running of the project. SC members are expected to participate in strategic planning, join monthly meetings, and approve changes to the governance model. The purpose of the SC is to ensure a smooth progress from the big-picture perspective. Indeed, changes that impact the full project require a synthetic analysis and a consensus that is both explicit and informed. In cases that the core contributor community (which includes the SC members) fails to reach such a consensus in the required time frame, the SC is the entity to resolve the issue.

The SC consists of community representatives and partner representatives. Community representatives of the SC are nominated by a core contributor. A nomination will result in a discussion that cannot take more than a month and then a vote by the core contributors which will stay open for a week. SC membership votes are subject to a two-third majority of all cast votes as well as a simple majority approval of all the current SC members.

Partner institutions who enter a collaboration agreement or sponsorship agreement with the OpenML Foundation can nominate a representative on the Steering Committee, if so agreed in the agreement. Such a collaboration should in principle include one full-time developer to work on OpenML (in cash or in kind) for the duration of the agreement. New partner representatives have to be confirmed by the SC following the same voting rules above.

The OpenML community must have at least equal footing in the steering committee. Additional SC members may be nominated to ensure this, following the membership voting rules described above.

When decisions are escalated to the steering committee (see the decision making process below), and no consensus can be found within a month, the SC can meet and decide by consensus or with a simple majority of all cast votes.

SC members who do not actively engage with the SC duties are expected to resign.

The current Steering Committee of OpenML consists of Bernd Bischl, Giuseppe Casalicchio, Matthias Feurer, Pieter Gijsbers, Jan van Rijn, and Joaquin Vanschoren. They all represent the OpenML community.

### Decision Making Process

Decisions about the future of the project are made through discussion with all members of the community. All non-sensitive project management discussion takes place on GitHub, on either project-wide or sub-project specific discussion boards or issue trackers. Occasionally, sensitive discussion occurs on the private core developer email list (see below). This includes voting on core/SC membership or discussion of internal disputes. All discussions must follow the [OpenML honor code](https://docs.openml.org/intro/terms/).

OpenML uses a “consensus seeking” process for making decisions. The group tries to find a resolution that has no open objections among core contributors. At any point during the discussion, any core contributors can call for a vote, which will conclude one month from the call for the vote, or when two thirds of all votes are in favor.

If no option can gather two thirds of the votes cast (ignoring abstentions), the decision is escalated to the SC, which in turn will use consensus seeking with the fallback option of a simple majority vote if no consensus can be found within a month. This is what we hereafter may refer to as “the decision making process”. It applies to all core OpenML repositories.

Decisions (in addition to adding core contributors and SC membership as above) are made according to the following rules:


Major changes:  

- Major changes, such as those that change the server API principles and metadata schema require a concrete proposal outlined in an OpenML Request for Comments (RfC), which has to be opened for public consultation for at least 1 month. The final version has to be approved using the decision-making process outlined above (two-third of the cast vote by core contributors or simple majority if escalated to the SC). Voting is typically done as a comment or reaction in the pull request (+1, -1, or 0 to abstain).  
- RfCs must be announced and shared via our communication channels and may link additional content (such as blog posts or google docs etc. detailing the changes).  
- Changes to the governance model use the same decision process outlined above.  

Other changes:  

- All other changes, such as corrections to text, bug fixes, maintenance work, or minor new features: requires one approved review by a core contributor, and no objections in the comments (lazy consensus). Core contributors are expected to give “reasonable time” to others to give their opinion on the pull request if they’re not confident others would agree. If an objection is raised, the proposer can appeal to the community and core contributors and the change can be approved or rejected using the decision making procedure outlined above. 
- Non-server packages that only have one core contributor are not subject to the ruling in the bullet point above (i.e. a sole core developer can make decisions on their own).

### Communication channels

OpenML uses the following communication channels:  

- The GitHub issue trackers and discussion boards.  
- A chat application for daily interaction with the community (currently Slack).  
- Private email lists (without archive) for the core developers (core@openml.org) and steering committee (steering@openml.org), for membership voting and sensitive discussions.  
- Biyearly Steering Committee meeting at predefined times, listed on the website, and asynchronous discussions on a discussion board. They are open to all steering committee members and core contributors, and they can all request discussion on a topic. Closed meetings for SC members only can be called in if there are sensitive discussions or other valid reasons.  
- A monthly Engineering meeting at predefined times, listed on the website. The meeting is open to all. Discussion points are put on the [project roadmap]  (https://github.com/orgs/openml/projects/2).
