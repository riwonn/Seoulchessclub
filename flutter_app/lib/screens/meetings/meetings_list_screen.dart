import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../providers/meeting_provider.dart';
import '../../models/meeting.dart';

class MeetingsListScreen extends StatefulWidget {
  const MeetingsListScreen({super.key});

  @override
  State<MeetingsListScreen> createState() => _MeetingsListScreenState();
}

class _MeetingsListScreenState extends State<MeetingsListScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MeetingProvider>().fetchMeetings();
    });
  }

  Future<void> _registerForMeeting(Meeting meeting) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('모임 참가'),
        content: Text('${meeting.title}에 참가하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('참가'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    try {
      await context.read<MeetingProvider>().registerForMeeting(meeting.id);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('모임 참가 신청이 완료되었습니다'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(e.toString().replaceAll('Exception: ', '')),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _registerInterest(Meeting meeting) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('관심 등록'),
        content: Text('${meeting.title}에 관심을 등록하시겠습니까?\n(결제 의사 표시)'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('등록'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    try {
      await context.read<MeetingProvider>().registerInterest(meeting.id);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('관심 등록이 완료되었습니다'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(e.toString().replaceAll('Exception: ', '')),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('모임 목록'),
      ),
      body: Consumer<MeetingProvider>(
        builder: (context, meetingProvider, child) {
          if (meetingProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (meetingProvider.error != null) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error_outline, size: 64, color: Colors.grey),
                    const SizedBox(height: 16),
                    Text(
                      '모임 목록을 불러올 수 없습니다',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      meetingProvider.error!,
                      style: Theme.of(context).textTheme.bodyMedium,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton.icon(
                      onPressed: () => meetingProvider.fetchMeetings(),
                      icon: const Icon(Icons.refresh),
                      label: const Text('다시 시도'),
                    ),
                  ],
                ),
              ),
            );
          }

          final meetings = meetingProvider.sortedMeetings;

          if (meetings.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.event_busy, size: 64, color: Colors.grey),
                  const SizedBox(height: 16),
                  Text(
                    '예정된 모임이 없습니다',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () => meetingProvider.fetchMeetings(),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: meetings.length,
              itemBuilder: (context, index) {
                final meeting = meetings[index];
                return _MeetingCard(
                  meeting: meeting,
                  onRegister: () => _registerForMeeting(meeting),
                  onRegisterInterest: () => _registerInterest(meeting),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class _MeetingCard extends StatelessWidget {
  final Meeting meeting;
  final VoidCallback onRegister;
  final VoidCallback onRegisterInterest;

  const _MeetingCard({
    required this.meeting,
    required this.onRegister,
    required this.onRegisterInterest,
  });

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('yyyy년 MM월 dd일 HH:mm');
    final occupancyPercent = (meeting.occupancyRate * 100).toInt();

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 제목
            Row(
              children: [
                Expanded(
                  child: Text(
                    meeting.title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
                if (!meeting.isAvailable)
                  Chip(
                    label: const Text('마감'),
                    backgroundColor: Colors.red.shade100,
                  ),
              ],
            ),
            const SizedBox(height: 12),
            
            // 날짜/시간
            Row(
              children: [
                const Icon(Icons.calendar_today, size: 16, color: Colors.grey),
                const SizedBox(width: 8),
                Text(dateFormat.format(meeting.dateTime)),
              ],
            ),
            const SizedBox(height: 8),
            
            // 장소
            Row(
              children: [
                const Icon(Icons.location_on, size: 16, color: Colors.grey),
                const SizedBox(width: 8),
                Text(meeting.location),
              ],
            ),
            const SizedBox(height: 12),
            
            // 정원 정보
            Row(
              children: [
                const Icon(Icons.people, size: 16, color: Colors.grey),
                const SizedBox(width: 8),
                Text(
                  '${meeting.currentParticipants}/${meeting.capacity}명',
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(width: 8),
                Text('($occupancyPercent% 찼음)'),
              ],
            ),
            const SizedBox(height: 8),
            
            // 진행 바
            LinearProgressIndicator(
              value: meeting.occupancyRate,
              backgroundColor: Colors.grey.shade200,
              valueColor: AlwaysStoppedAnimation<Color>(
                meeting.isAvailable ? Colors.blue : Colors.red,
              ),
            ),
            const SizedBox(height: 16),
            
            // 버튼
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: meeting.isAvailable ? onRegisterInterest : null,
                    child: const Text('관심 등록'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: meeting.isAvailable ? onRegister : null,
                    child: const Text('참가 신청'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

