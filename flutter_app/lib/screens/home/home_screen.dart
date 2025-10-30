import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';
import '../../providers/meeting_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    // 화면 로드 시 모임 목록 불러오기
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MeetingProvider>().fetchMeetings();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Community Control'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () => context.go('/profile'),
          ),
        ],
      ),
      body: Consumer2<AuthProvider, MeetingProvider>(
        builder: (context, authProvider, meetingProvider, child) {
          final user = authProvider.currentUser;
          final meetings = meetingProvider.sortedMeetings;

          return RefreshIndicator(
            onRefresh: () => meetingProvider.fetchMeetings(),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 환영 메시지
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '환영합니다, ${user?.name ?? '사용자'}님!',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            '총 방문 횟수: ${user?.totalVisits ?? 0}회',
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            '참여한 모임: ${user?.attendedMeetings?.length ?? 0}개',
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // 빠른 메뉴
                  Row(
                    children: [
                      Expanded(
                        child: _QuickMenuButton(
                          icon: Icons.event,
                          label: '모임 목록',
                          onTap: () => context.go('/meetings'),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _QuickMenuButton(
                          icon: Icons.person,
                          label: '내 프로필',
                          onTap: () => context.go('/profile'),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // 다가오는 모임
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        '다가오는 모임',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      TextButton(
                        onPressed: () => context.go('/meetings'),
                        child: const Text('전체 보기'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  
                  if (meetingProvider.isLoading)
                    const Center(
                      child: Padding(
                        padding: EdgeInsets.all(32.0),
                        child: CircularProgressIndicator(),
                      ),
                    )
                  else if (meetingProvider.error != null)
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.all(32.0),
                        child: Column(
                          children: [
                            const Icon(Icons.error_outline, size: 48, color: Colors.grey),
                            const SizedBox(height: 16),
                            Text(
                              '모임 목록을 불러올 수 없습니다',
                              style: Theme.of(context).textTheme.bodyLarge,
                            ),
                            const SizedBox(height: 8),
                            Text(
                              meetingProvider.error!,
                              style: Theme.of(context).textTheme.bodySmall,
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    )
                  else if (meetings.isEmpty)
                    const Center(
                      child: Padding(
                        padding: EdgeInsets.all(32.0),
                        child: Text('예정된 모임이 없습니다'),
                      ),
                    )
                  else
                    ...meetings.take(3).map((meeting) {
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          leading: CircleAvatar(
                            child: Text('${meeting.currentParticipants}/${meeting.capacity}'),
                          ),
                          title: Text(meeting.title),
                          subtitle: Text(
                            '${_formatDateTime(meeting.dateTime)}\n${meeting.location}',
                          ),
                          isThreeLine: true,
                          trailing: Icon(
                            meeting.isAvailable
                                ? Icons.arrow_forward_ios
                                : Icons.block,
                            size: 16,
                          ),
                          onTap: () => context.go('/meetings'),
                        ),
                      );
                    }),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  String _formatDateTime(DateTime dateTime) {
    return '${dateTime.year}년 ${dateTime.month}월 ${dateTime.day}일 '
        '${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
  }
}

class _QuickMenuButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _QuickMenuButton({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              Icon(icon, size: 48, color: Theme.of(context).primaryColor),
              const SizedBox(height: 12),
              Text(
                label,
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

