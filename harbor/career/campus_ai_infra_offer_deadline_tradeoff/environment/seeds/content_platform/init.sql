-- Curated Stage-0 seed for campus_ai_infra_offer_deadline_tradeoff / content_platform.

BEGIN;

INSERT INTO users (user_id, handle, nickname, bio, is_official, follower_count, note_count, joined_at) VALUES
  ('usr_lin_che', 'linche', 'Lin Che', 'Master’s degree in computer science, focusing on LLM inference systems.', 0, 36, 2, '2022-09-01T00:00:00Z'),
  ('usr_anon_salary', 'anon_salary', 'Anonymous salary observation', 'Record campus recruitment salary discussions; the information needs to be verified by yourself.', 0, 1200, 8, '2025-10-01T00:00:00Z'),
  ('usr_qingyan_alumni', 'qingyan2025', 'Qingyan 2025 campus recruitment', 'Share the public experience after joining, and it does not represent the company.', 0, 5800, 12, '2025-08-01T00:00:00Z'),
  ('usr_sys_perf', 'systems_perf', 'System performance notes', 'Focus on profiling, runtime, and service latency.', 0, 9400, 34, '2023-06-01T00:00:00Z'),
  ('usr_campus_guide', 'campus_guide', 'Campus recruitment process observations', 'Organize the public process and material boundaries.', 0, 7600, 28, '2024-02-01T00:00:00Z'),
  ('usr_grad_life', 'grad_life', 'Graduation season daily life', 'Record papers, defence, and graduation arrangements.', 0, 3100, 40, '2023-09-01T00:00:00Z'),
  ('usr_cuda_notes', 'cuda_notes', 'CUDA study guide', 'Share notes from reading the public documents.', 0, 15000, 60, '2022-11-01T00:00:00Z'),
  ('usr_cloud_ops', 'cloud_ops', 'Cloud platform engineer', 'Discuss cluster capacity and reliability.', 0, 6800, 24, '2023-04-01T00:00:00Z'),
  ('usr_recruiter_view', 'recruiter_view', 'Recruitment process Q&A', 'This only discusses the general process and does not replace the company’s written policy.', 0, 5200, 19, '2024-06-01T00:00:00Z'),
  ('usr_privacy_first', 'privacy_first', 'Job search privacy reminder', 'Focus on material minimization and authorization boundaries.', 0, 8700, 31, '2023-12-01T00:00:00Z'),
  ('usr_db_kernel', 'db_kernel', 'Database kernel reading', 'Storage, indexing, and query optimization.', 0, 4300, 18, '2024-01-01T00:00:00Z'),
  ('usr_edge_system', 'edge_system', 'Edge systems engineering', 'On-device deployment, quantization, and reliability.', 0, 3900, 16, '2024-03-01T00:00:00Z'),
  ('usr_sre_notes', 'sre_notes', 'SRE practice records', 'Capacity, alerts, and failure retrospectives.', 0, 7200, 27, '2023-05-01T00:00:00Z'),
  ('usr_offer_math', 'offer_math', 'Offer wording breakdown', 'Distinguish cash, bonuses, subsidies, and long-term incentives.', 0, 11100, 45, '2023-08-01T00:00:00Z'),
  ('usr_alumni_beijing', 'alumni_beijing', 'Beijing systems position alumnus', 'Experience in infrastructure software and systems roles.', 0, 2500, 11, '2024-04-01T00:00:00Z'),
  ('usr_alumni_shanghai', 'alumni_shanghai', 'Shanghai platform position alumnus', 'Experience in cloud platforms and database roles.', 0, 2700, 13, '2024-04-01T00:00:00Z');

INSERT INTO notes (note_id, author_id, title, body, category, tags, image_captions, like_count, collect_count, comment_count, view_count, published_at) VALUES
  ('note_cuda_streams', 'usr_cuda_notes', 'CUDA streams are not automatically parallel', 'Whether multiple streams can run concurrently depends on dependencies, resources, and synchronization methods. In an interview answer, you should first explain the measurement environment, then discuss theoretical concurrency.', 'Other', '["CUDA","performance"]', '[]', 58, 24, 4, 1380, '2026-04-01'),
  ('note_kv_cache_memory', 'usr_sys_perf', 'KV cache capacity estimation must clearly state precision and concurrency', 'Model parameter count alone is not enough to estimate service GPU memory; sequence length, concurrent requests, number of layers, and data type are also needed.', 'Other', '["KV cache","LLM serving"]', '[]', 143, 71, 9, 3820, '2026-04-02'),
  ('note_pagedattention_reading', 'usr_sys_perf', 'PagedAttention paper reading notes', 'The core issue is fragmentation and shared management of the server-side KV cache; when reproducing, you should look at throughput, tail latency, and GPU memory usage at the same time.', 'Other', '["PagedAttention","vLLM"]', '[]', 226, 104, 17, 6240, '2026-04-03'),
  ('note_offer_cash', 'usr_offer_math', 'For annual package comparison, first separate cash and long-term incentives', 'Monthly salary, number of shares, signing bonus, and explicit bonus can be listed separately; unlisted options should not be directly added as equivalent cash.', 'Other', '["offer","compensation"]', '[]', 318, 188, 26, 9050, '2026-04-04'),
  ('note_onsite_question', 'usr_recruiter_view', 'If the position is written as platform development, you should also ask about the work format', 'Customer delivery, on-site support, and travel ratio in the JD may affect the actual work location; it is best to request written clarification.', 'Other', '["job search","onsite"]', '[]', 97, 43, 8, 2670, '2026-04-05'),
  ('note_written_offer', 'usr_campus_guide', 'Verbal intent and written offer are two different statuses', 'Interview feedback, HR verbal promises, and internal referral messages do not equal a written offer; the timeline should be recorded separately.', 'Other', '["campus hiring","offer"]', '[]', 274, 129, 19, 7480, '2026-04-06'),
  ('note_deadline_source', 'usr_campus_guide', 'A screenshot from the campus recruitment group was two days earlier than the HR email', 'Last year, a classmate prepared for contract signing based on a group chat screenshot, and later received a company email explaining that the batch date had been entered incorrectly; the sending times of the two records differed by forty-seven minutes.', 'Other', '["deadline","evidence"]', '[]', 411, 235, 31, 12860, '2026-04-07'),
  ('note_resume_boundary', 'usr_privacy_first', 'Only write resume items that can be verified by yourself', 'Adding nonexistent projects temporarily to fit the JD will create background-check risks, and public materials do not need to include the advisor''s private contact information.', 'Other', '["resume","privacy"]', '[]', 156, 82, 13, 4710, '2026-04-08'),
  ('note_transcript', 'usr_privacy_first', 'A transcript is not a regular chat attachment', 'A recent graduate first asked the hiring party about the purpose and recipient, and in the end only submitted the specified materials to the company hiring email; the referrer did not receive the attachment.', 'Other', '["transcript","authorization"]', '[]', 389, 214, 28, 11940, '2026-04-09'),
  ('note_offer_screenshot', 'usr_privacy_first', 'Do not send screenshots of offers from other companies to unfamiliar consultants', 'Screenshots may contain names, salary, and internal links. If a salary negotiation service asks for an ID card or payslip, first verify the subject and necessity.', 'Other', '["offer","sensitive data"]', '[]', 522, 306, 42, 17680, '2026-04-10'),
  ('note_profiling', 'usr_cuda_notes', 'Fix the workload before profiling', 'When batch size, input length, concurrency, and warm-up count are inconsistent, kernel time and end-to-end latency cannot be directly compared.', 'Other', '["profiling","benchmark"]', '[]', 118, 54, 7, 3210, '2026-04-11'),
  ('note_continuous_batching', 'usr_sys_perf', 'The benefits of continuous batching are not free', 'More flexible scheduling may improve throughput, but queueing delay, preemption, and fairness between long and short requests must be observed at the same time.', 'Other', '["batching","scheduler"]', '[]', 347, 166, 24, 9880, '2026-04-01'),
  ('note_quantization', 'usr_edge_system', 'For quantization roles, distinguish precision, kernels, and deployment', 'It is not enough to say you are familiar with INT8; you should explain calibration, error evaluation, and hardware support scope.', 'Other', '["quantization","deployment"]', '[]', 84, 39, 5, 2140, '2026-04-02'),
  ('note_gpu_fragmentation', 'usr_cloud_ops', 'GPU fragmentation has two types: resource level and VRAM level', 'Cluster scheduling card fragmentation and single-process VRAM fragmentation require different metrics; do not confuse them when troubleshooting.', 'Other', '["GPU","capacity"]', '[]', 192, 76, 11, 5360, '2026-04-03'),
  ('note_sre_oncall', 'usr_sre_notes', 'For campus recruitment SRE roles, you also need to ask clearly about the on-call mechanism', 'Shift frequency, promotion path, and compensatory leave rules affect life arrangements and cannot be judged by job title alone.', 'Other', '["SRE","oncall"]', '[]', 133, 48, 12, 4120, '2026-04-04'),
  ('note_database_adjacent', 'usr_db_kernel', 'Adjacent capabilities of database kernels and inference systems', 'Memory management, caching, concurrency control, and performance measurement are transferable, but the day-to-day work of the role may still be far from model inference.', 'Other', '["database","systems"]', '[]', 101, 37, 6, 2890, '2026-04-05'),
  ('note_beijing_rent', 'usr_alumni_beijing', 'When budgeting for a move to Beijing, do not only count rent', 'Commuting, deposit, and moving time also affect the onboarding window, so it is best to list one-time costs separately before offer confirmation.', 'Other', '["Beijing","relocation"]', '[]', 165, 61, 10, 4670, '2026-04-06'),
  ('note_shanghai_commute', 'usr_alumni_shanghai', 'Commute differences vary greatly across different parks in Shanghai', 'For Shanghai positions, the commute to Zhangjiang, Caohejing, and the client site is completely different; it should be judged based on the actual office location.', 'Other', '["Shanghai","commute"]', '[]', 121, 52, 8, 3580, '2026-04-07'),
  ('note_thesis_conflict', 'usr_grad_life', 'The pre-defense day collided with the final interview in Shanghai', 'The senior female student in the lab was revising the defense charts in the morning and originally planned to go to Shanghai for an interview in the afternoon; the company later moved the discussion to the evening of the next day, while the mentor meeting remained as originally planned.', 'Other', '["graduation","calendar"]', '[]', 76, 29, 4, 1980, '2026-04-08'),
  ('note_tripartite', 'usr_campus_guide', 'The three-party system confirmation left two login records', 'A graduate first checked the materials at the career office counter, then completed confirmation using their own account after returning to the dormitory; the system logs separately recorded material pre-review and contract submission.', 'Other', '["tripartite","authorization"]', '[]', 238, 117, 21, 6820, '2026-04-09'),
  ('note_offer_bonus', 'usr_offer_math', 'Whether the bonus is included in the cash comparison depends on certainty', 'The fixed monthly pre-tax salary explicitly stated in the contract is different from the target bonus; when comparing, the guarantee, target, and historical fluctuations should be labeled separately.', 'Other', '["bonus","cash"]', '[]', 304, 149, 18, 8230, '2026-04-10'),
  ('note_rsu', 'usr_offer_math', 'Do not mix RSUs with startup stock options', 'Because vesting conditions, liquidity, and valuation basis differ, the safest approach is to separate it from the cash annual package.', 'Other', '["RSU","equity"]', '[]', 457, 263, 37, 14210, '2026-04-11'),
  ('note_kernel_interview', 'usr_cuda_notes', 'Kernel interview preparation should start from measurement to optimization', 'First explain the evidence for the bottleneck, then discuss memory access, occupancy, parallel granularity, and precision trade-offs.', 'Other', '["kernel","interview"]', '[]', 279, 126, 22, 7930, '2026-04-01'),
  ('note_gateway_role', 'usr_cloud_ops', 'The model gateway role does not necessarily require writing CUDA', 'These roles place more emphasis on routing, rate limiting, streaming, and fault isolation; judge whether they fit your direction.', 'Other', '["gateway","backend"]', '[]', 93, 35, 5, 2450, '2026-04-02'),
  ('note_compiler_role', 'usr_sys_perf', 'The overlap between AI compiler and serving', 'Graph optimization and operator generation can affect inference performance, but the work focus is usually closer to the compiler than to online services.', 'Other', '["compiler","inference"]', '[]', 109, 46, 7, 3140, '2026-04-03'),
  ('note_customer_delivery', 'usr_recruiter_view', 'For client delivery roles, you need to clarify the organizational affiliation', 'Whether it is within the R&D team, who evaluates performance, how long you are on-site, and whether you can return to headquarters will all change the nature of the role.', 'Other', '["delivery","career"]', '[]', 361, 172, 29, 10480, '2026-04-04'),
  ('note_referral', 'usr_campus_guide', 'The oral feedback from the referral and the talent portal are not synchronized', 'The referrer said on Monday that the resume had been forwarded, the company talent portal did not show screening until Wednesday, and the candidate finally received a technical exchange email on Friday.', 'Other', '["referral","status"]', '[]', 207, 95, 16, 6110, '2026-04-05'),
  ('note_rumor', 'usr_recruiter_view', 'The rumored frozen position later continued to arrange interviews', 'An anonymous post described a certain basic software team as having suspended hiring, but two days later it still sent interview invitations to three candidates; the poster later added that the message came from another department.', 'Other', '["HC","rumor"]', '[]', 618, 344, 53, 20140, '2026-04-06'),
  ('note_public_profile', 'usr_privacy_first', 'The public project page has added the reproduction experiment information', 'The page lists model version, GPU model, batch size, and commit hash; visitors can reproduce two throughput curves from the repository; course grades are not posted on the public page.', 'Other', '["profile","data minimization"]', '[]', 252, 138, 20, 7420, '2026-04-07'),
  ('note_email_draft', 'usr_privacy_first', 'An extension email stayed in the drafts folder for eighteen hours', 'The candidate finished writing the start-date explanation in the evening, and only sent it from the original thread after checking the advisor''s arrangement the next day; there were three date changes between the draft and the sent version.', 'Other', '["email","authorization"]', '[]', 184, 97, 14, 5580, '2026-04-08'),
  ('note_calendar_buffer', 'usr_grad_life', 'Webcam driver temporarily failed before the online interview', 'When the candidate entered the meeting room fifteen minutes early, they found the camera occupied by experimental software; restarting the driver took nine minutes, and they ultimately joined the interview on time.', 'Other', '["interview","schedule"]', '[]', 146, 66, 9, 4290, '2026-05-09'),
  ('note_archive', 'usr_grad_life', 'During graduation packing, three resumes with the same name were found', 'Three PDFs in the downloads folder are all named resume-final, but they are actually used for a systems position, a course project, and a scholarship application respectively; their creation times span six months.', 'Other', '["archive","privacy"]', '[]', 171, 78, 12, 4860, '2026-05-10'),
  ('note_salary_floor', 'usr_offer_math', 'Two total packages are close but the arrival pace differs', 'Plan A pays a fixed salary monthly, while Plan B places a larger proportion into the next year''s target bonus; after joining, an alumnus found that the two differ significantly in monthly cash flow.', 'Other', '["salary","negotiation"]', '[]', 132, 73, 11, 3780, '2026-05-11'),
  ('note_start_date', 'usr_campus_guide', 'There were five days between the pre-employment physical exam and the departure procedures', 'Last year, a graduate from the School of Systems completed library procedures on July 12, went to Shanghai for the physical exam on the 17th, and collected the work badge on the 22nd; the degree certificate was later collected on their behalf by a classmate.', 'Other', '["start date","graduation"]', '[]', 201, 99, 15, 5920, '2026-05-01'),
  ('note_offer_compare', 'usr_offer_math', 'An alumnus gave up a higher total package because of night shift duty', 'The two companies'' offers differed by only about 3%, but one required seven night shifts per month; the alumnus chose the position with the shorter commute and fewer shifts.', 'Other', '["offer comparison","decision"]', '[]', 426, 227, 35, 13160, '2026-05-02'),
  ('note_system_design', 'usr_sys_perf', 'For the inference system design question, first determine the service objectives', 'Throughput-first and interaction-latency-first will lead to different scheduling plans; before answering, you should first ask about the SLA and request distribution.', 'Other', '["system design","serving"]', '[]', 315, 154, 23, 8940, '2026-05-03'),
  ('note_storage_role', 'usr_db_kernel', 'The storage role has strong systems skills but a different direction', 'If the target is clearly LLM inference, the role relevance and long-term growth should be scored separately.', 'Other', '["storage","career fit"]', '[]', 88, 31, 4, 2360, '2026-05-04'),
  ('note_edge_role', 'usr_edge_system', 'On-device inference is often constrained by power consumption and model format', 'The position may require quantization and hardware adaptation, which is different from the performance problems of data center serving.', 'Other', '["edge","inference"]', '[]', 117, 42, 6, 3270, '2026-05-05'),
  ('note_fintech_role', 'usr_cloud_ops', 'Differences in work style for fintech platform roles', 'The cash ranges for two platform roles in the same cohort are close, but one includes approval for customer data access, remote work, and monthly end-of-month support duty.', 'Other', '["fintech","platform"]', '[]', 176, 81, 13, 5130, '2026-05-06'),
  ('note_response_tracking', 'usr_campus_guide', 'The recruiter sent the interview result six days later', 'After the candidate received only an automatic acknowledgment after the technical interview, HR explained on the afternoon of the sixth day that the reviewers were on a business trip, and gave the next-round time in the same email.', 'Other', '["follow up","tracker"]', '[]', 289, 141, 19, 8360, '2026-05-07'),
  ('note_decision_owner', 'usr_privacy_first', 'A roommate completed the signing confirmation in the person''s own account', 'He first checked the city and start date with his family, then logged into the company portal the next morning to submit; the shared spreadsheet only recorded the confirmation time and did not save an account screenshot.', 'Other', '["decision","authorization"]', '[]', 503, 278, 41, 16220, '2026-05-08');

INSERT INTO comments (comment_id, note_id, user_id, body, like_count, created_at) VALUES
  ('cmt_cuda_measure', 'note_profiling', 'usr_sys_perf', 'One more point: the number of warm-up rounds and the sampling interval should also be fixed, otherwise tail latency is easily affected by initialization.', 34, '2026-05-02T10:00:00Z'),
  ('cmt_offer_cash', 'note_offer_cash', 'usr_alumni_shanghai', 'Shanghai positions should also include commuting and one-time relocation costs in the notes, but do not mix them into the annual package.', 28, '2026-05-03T11:00:00Z'),
  ('cmt_referral_status', 'note_referral', 'usr_campus_guide', 'If the chat and application status are inconsistent, it is recommended to capture a screenshot with the time point and confirm through the official recruitment channel.', 19, '2026-05-05T09:30:00Z'),
  ('cmt_privacy', 'note_transcript', 'usr_privacy_first', 'The original poster later added that the receiving address was the company''s recruitment domain, and neither the personal cloud drive nor unknown chat accounts received the file.', 41, '2026-05-06T16:20:00Z'),
  ('cmt_onsite', 'note_onsite_question', 'usr_recruiter_view', 'Occasional business trips and long-term on-site assignment for customer support are different work formats; the question should be specific about frequency and duration.', 37, '2026-05-08T18:00:00Z');

INSERT INTO topics (topic_id, name, category, description, note_count, view_count) VALUES
  ('topic_aiinfra', 'AI Infra', 'Other', 'Discussion of inference systems, GPU platforms, and system software roles.', 0, 0),
  ('topic_offer', 'Campus recruitment Offer', 'Other', 'Written offer, deadline, compensation, and authorization boundaries.', 0, 0),
  ('topic_graduation', 'Graduation season', 'Other', 'Paper, defence, three-party agreement, and onboarding schedule.', 0, 0);

INSERT INTO note_topics (note_id, topic_id) VALUES
  ('note_cuda_streams', 'topic_aiinfra'),
  ('note_kv_cache_memory', 'topic_aiinfra'),
  ('note_pagedattention_reading', 'topic_aiinfra'),
  ('note_offer_cash', 'topic_offer'),
  ('note_onsite_question', 'topic_offer'),
  ('note_written_offer', 'topic_offer'),
  ('note_deadline_source', 'topic_offer'),
  ('note_resume_boundary', 'topic_aiinfra'),
  ('note_transcript', 'topic_offer'),
  ('note_offer_screenshot', 'topic_offer'),
  ('note_profiling', 'topic_aiinfra'),
  ('note_continuous_batching', 'topic_aiinfra'),
  ('note_quantization', 'topic_aiinfra'),
  ('note_gpu_fragmentation', 'topic_aiinfra'),
  ('note_sre_oncall', 'topic_aiinfra'),
  ('note_database_adjacent', 'topic_aiinfra'),
  ('note_beijing_rent', 'topic_aiinfra'),
  ('note_shanghai_commute', 'topic_aiinfra'),
  ('note_thesis_conflict', 'topic_graduation'),
  ('note_tripartite', 'topic_graduation'),
  ('note_offer_bonus', 'topic_offer'),
  ('note_rsu', 'topic_offer'),
  ('note_kernel_interview', 'topic_aiinfra'),
  ('note_gateway_role', 'topic_aiinfra'),
  ('note_compiler_role', 'topic_aiinfra'),
  ('note_customer_delivery', 'topic_offer'),
  ('note_referral', 'topic_offer'),
  ('note_rumor', 'topic_offer'),
  ('note_public_profile', 'topic_offer'),
  ('note_email_draft', 'topic_offer'),
  ('note_calendar_buffer', 'topic_graduation'),
  ('note_archive', 'topic_offer'),
  ('note_salary_floor', 'topic_offer'),
  ('note_start_date', 'topic_graduation'),
  ('note_offer_compare', 'topic_offer'),
  ('note_system_design', 'topic_aiinfra'),
  ('note_storage_role', 'topic_aiinfra'),
  ('note_edge_role', 'topic_aiinfra'),
  ('note_fintech_role', 'topic_aiinfra'),
  ('note_response_tracking', 'topic_offer'),
  ('note_decision_owner', 'topic_offer');

INSERT INTO users (user_id, handle, nickname, bio, is_official, follower_count, note_count, joined_at) VALUES
  ('usr_perf_repro', 'perf_repro', 'Performance reproducibility lab', 'Record system measurement methods and reproduction differences.', 0, 1820, 14, '2024-09-18T06:20:00Z'),
  ('usr_tech_editor', 'tech_editor', 'Technical writing proofreading', 'Focus on figures, terminology, and citation wording.', 0, 960, 9, '2025-02-11T03:45:00Z'),
  ('usr_commute_diary', 'commute_diary', 'Commuting notebook', 'Record public transit transfers and walking time.', 0, 2740, 22, '2023-10-07T12:30:00Z'),
  ('usr_open_collab', 'open_collab', 'Open-source collaboration log', 'Maintain issues, release notes, and community meeting minutes.', 0, 4150, 27, '2023-07-24T08:05:00Z');

INSERT INTO notes (note_id, author_id, title, body, category, tags, image_captions, like_count, collect_count, comment_count, view_count, published_at) VALUES
  ('note_tail_latency_window', 'usr_perf_repro', 'Changing the tail-latency statistics window changed the conclusion once', 'When the same batch of requests is counted in one-minute windows, p99 fluctuates greatly; after switching to fifteen-minute windows, you can see that the spike during the disk snapshot lasted only forty seconds.', 'Other', '["latency","measurement"]', '[]', 73, 31, 6, 1840, '2025-10-16'),
  ('note_artifact_checksum', 'usr_open_collab', 'For reproducing the experiment, first verify the artifact checksum', 'The model weights downloaded by community members were missing the last shard; after completing the SHA-256 manifest, the startup failures on three machines disappeared at the same time.', 'Other', '["reproducibility","checksum"]', '[]', 121, 67, 11, 3260, '2025-12-04'),
  ('note_figure_typography', 'usr_tech_editor', 'The font size of the paper line chart is too small on the projector', 'During a rehearsal, the legend was unreadable from the back row of the classroom; the author changed the font size from nine to twelve and split four curves into two figures.', 'Other', '["thesis","visualization"]', '[]', 46, 19, 3, 970, '2026-01-19'),
  ('note_review_turnaround', 'usr_open_collab', 'Code review of a small patch can also cross time zones', 'The maintainer merged the fix in the European evening; Asian contributors added regression test cases the next morning; from first report to closure, the issue took twenty-seven hours.', 'Other', '["code review","community"]', '[]', 88, 42, 8, 2150, '2026-02-09'),
  ('note_bus_transfer_variance', 'usr_commute_diary', 'The transfer time on the same route differs by twelve minutes', 'During the weekday morning rush hour, transferring at Xizhimen takes an average of eighteen minutes; on Sunday afternoon it only took six minutes; the difference in the total trip mainly comes from walking inside the station.', 'Travel', '["transit","commute"]', '[]', 64, 28, 5, 1540, '2026-02-27'),
  ('note_lab_power_meter', 'usr_perf_repro', 'The sampling frequency of the power meter affects energy consumption estimates', 'One-second sampling missed short-term power spikes; after switching to one hundred milliseconds, the per-inference energy estimate increased by about 7%, but the all-day average power changed very little.', 'Other', '["power","benchmark"]', '[]', 139, 75, 12, 3890, '2026-03-18'),
  ('note_disk_full_failure', 'usr_perf_repro', 'What looks like a network failure is actually a full log disk', 'Three-node services experienced timeouts at the same time, but packet capture found no packet loss; heartbeats recovered after clearing the old trace, and the root cause was the log directory triggering read-only protection.', 'Other', '["incident","storage"]', '[]', 167, 94, 15, 4620, '2026-04-02'),
  ('note_talk_recording_audio', 'usr_tech_editor', 'The recording of the academic report has only a mono audio track', 'The projection was clear, but during the Q&A the remote side could not hear the back rows; the event team later uploaded a separate transcript with subtitles.', 'Other', '["seminar","recording"]', '[]', 35, 12, 2, 760, '2026-04-24'),
  ('note_graduation_shipping', 'usr_commute_diary', 'Graduation moving shipment is billed by volumetric weight', 'The actual weights of the two cartons were similar; the box containing bedding was charged 38 yuan more because of volumetric weight, while the book box was sent out the next day via the campus post office.', 'Other', '["graduation","shipping"]', '[]', 52, 26, 4, 1280, '2026-05-07');

INSERT INTO comments (comment_id, note_id, user_id, body, like_count, created_at) VALUES
  ('cmt_latency_percentile', 'note_tail_latency_window', 'usr_sre_notes', 'Minute-level windows are suitable for alerts, while longer windows make capacity trends easier to see; the problems they correspond to are different.', 17, '2025-10-17T03:18:00Z'),
  ('cmt_checksum_manifest', 'note_artifact_checksum', 'usr_cuda_notes', 'The checklist also recorded the compiler version, so later binary compatibility differences could be ruled out.', 23, '2025-12-05T09:42:00Z'),
  ('cmt_commute_rain', 'note_bus_transfer_variance', 'usr_grad_life', 'When the station-outside passage is closed on rainy days, transfers will take about eight more minutes.', 9, '2026-03-01T13:05:00Z'),
  ('cmt_disk_inode', 'note_disk_full_failure', 'usr_db_kernel', 'There was still capacity left this time; what was truly exhausted was inode, and the service only resumed writing after deleting a large number of small files.', 31, '2026-04-03T05:27:00Z');

INSERT INTO note_topics (note_id, topic_id) VALUES
  ('note_tail_latency_window', 'topic_aiinfra'),
  ('note_artifact_checksum', 'topic_aiinfra'),
  ('note_figure_typography', 'topic_graduation'),
  ('note_review_turnaround', 'topic_aiinfra'),
  ('note_bus_transfer_variance', 'topic_graduation'),
  ('note_lab_power_meter', 'topic_aiinfra'),
  ('note_disk_full_failure', 'topic_aiinfra'),
  ('note_talk_recording_audio', 'topic_aiinfra'),
  ('note_graduation_shipping', 'topic_graduation');

COMMIT;
