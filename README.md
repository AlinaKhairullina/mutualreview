Mutual reviews
=
Subject area
- 

 *Code Review* is one of the important stages of the software development life cycle. Sometimes teams have separate programmers who review the code and are responsible for the quality of the source code entering the repositories. But most often in teams, code review is mutual, that is, developers simultaneously write code and review the code of their colleagues.


According to published research data from large companies, the share of working time on code review reaches 20%. Most programmers treat this procedure responsibly, but there are cases when two developers agree and give positive ratings to each other’s uploaded code. **`You - to me, I - to you,`** without a detailed and thorough analysis of the source code. Such cases must be identified; this is the responsibility of team and project leaders. Moreover, this process can be automated, identifying suspicious mutual reviews for further discussion within the team.

Target
-
Develop and implement a software system that detects suspicious mutual code reviews.

Input data
-
The data is a sequence of records of positive code reviews. Jsonl text format, each line of which contains one event and is described by three main parameters:
- **timestamp**: time of publication of the review
- **author**: commit author
- **reviewer**: reviewer who left a positive rating

*For an example of input data in the `data` folder there is a file with a small dataset `small_data.jsonl`*

Output
-
A list of pairs of users sorted by *“danger”* and the time of their mutual code reviews.

***The task was completed before studying the Numpy and Pandas libraries***
