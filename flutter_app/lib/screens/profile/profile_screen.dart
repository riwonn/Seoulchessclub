import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../../providers/auth_provider.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  String _getChessExperienceText(String experience) {
    switch (experience) {
      case 'NO_BUT_WANT_TO_LEARN':
        return '아니요, 배우고 싶어요';
      case 'KNOW_RULES_ONLY':
        return '규칙만 알아요';
      case 'OCCASIONALLY_PLAY':
        return '가끔 둡니다';
      case 'PLAY_WELL':
        return '잘 둡니다';
      default:
        return experience;
    }
  }

  String _getChessRatingText(String? rating) {
    if (rating == null) return '미설정';
    switch (rating) {
      case 'I_DONT_KNOW':
        return '모르겠어요';
      case 'UNDER_1000':
        return '1000 이하';
      case 'BETWEEN_1000_1500':
        return '1000-1500';
      case 'BETWEEN_1500_2000':
        return '1500-2000';
      case 'OVER_2000':
        return '2000 이상';
      default:
        return rating;
    }
  }

  String _getGenderText(String gender) {
    switch (gender) {
      case 'MALE':
        return '남성';
      case 'FEMALE':
        return '여성';
      case 'OTHER':
        return '기타';
      default:
        return gender;
    }
  }

  Future<void> _logout(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('로그아웃'),
        content: const Text('정말 로그아웃하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('로그아웃'),
          ),
        ],
      ),
    );

    if (confirmed != true) return;

    await context.read<AuthProvider>().logout();
    
    if (context.mounted) {
      context.go('/auth/phone');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('내 프로필'),
      ),
      body: Consumer<AuthProvider>(
        builder: (context, authProvider, child) {
          final user = authProvider.currentUser;

          if (user == null) {
            return const Center(
              child: Text('사용자 정보를 불러올 수 없습니다'),
            );
          }

          return RefreshIndicator(
            onRefresh: () => authProvider.refreshUser(),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 프로필 헤더
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Row(
                        children: [
                          CircleAvatar(
                            radius: 40,
                            backgroundColor: Theme.of(context).primaryColor,
                            child: Text(
                              user.name[0].toUpperCase(),
                              style: const TextStyle(
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  user.name,
                                  style: Theme.of(context).textTheme.headlineSmall,
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  user.email,
                                  style: Theme.of(context).textTheme.bodyMedium,
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  user.phoneNumber,
                                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: Colors.grey,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // 통계
                  Text(
                    '활동 통계',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: _StatCard(
                          icon: Icons.event_available,
                          label: '총 방문',
                          value: '${user.totalVisits}회',
                          color: Colors.blue,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _StatCard(
                          icon: Icons.people,
                          label: '참여 모임',
                          value: '${user.attendedMeetings?.length ?? 0}개',
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // 회원 정보
                  Text(
                    '회원 정보',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 12),
                  Card(
                    child: Column(
                      children: [
                        _InfoTile(
                          icon: Icons.people,
                          label: '성별',
                          value: _getGenderText(user.gender),
                        ),
                        const Divider(height: 1),
                        _InfoTile(
                          icon: Icons.cake,
                          label: '출생년도',
                          value: user.birthYear?.toString() ?? '미설정',
                        ),
                        const Divider(height: 1),
                        _InfoTile(
                          icon: Icons.extension,
                          label: '체스 경험',
                          value: _getChessExperienceText(user.chessExperience),
                        ),
                        const Divider(height: 1),
                        _InfoTile(
                          icon: Icons.star,
                          label: '체스 레이팅',
                          value: _getChessRatingText(user.chessRating),
                        ),
                        const Divider(height: 1),
                        _InfoTile(
                          icon: Icons.calendar_today,
                          label: '가입일',
                          value: DateFormat('yyyy년 MM월 dd일').format(user.createdAt),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // 참여한 모임
                  if (user.attendedMeetings != null && user.attendedMeetings!.isNotEmpty) ...[
                    Text(
                      '참여한 모임',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 12),
                    Card(
                      child: ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: user.attendedMeetings!.length,
                        separatorBuilder: (context, index) => const Divider(height: 1),
                        itemBuilder: (context, index) {
                          final meeting = user.attendedMeetings![index];
                          return ListTile(
                            leading: CircleAvatar(
                              backgroundColor: meeting.status == 'CONFIRMED'
                                  ? Colors.green
                                  : Colors.orange,
                              child: Icon(
                                meeting.status == 'CONFIRMED'
                                    ? Icons.check
                                    : Icons.pending,
                                color: Colors.white,
                              ),
                            ),
                            title: Text('모임 #${meeting.meetingId}'),
                            subtitle: Text(
                              DateFormat('yyyy-MM-dd').format(meeting.registeredAt),
                            ),
                            trailing: Chip(
                              label: Text(
                                meeting.status == 'CONFIRMED' ? '확정' : '대기중',
                                style: const TextStyle(fontSize: 12),
                              ),
                              backgroundColor: meeting.status == 'CONFIRMED'
                                  ? Colors.green.shade100
                                  : Colors.orange.shade100,
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],
                  
                  // 로그아웃 버튼
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () => _logout(context),
                      icon: const Icon(Icons.logout),
                      label: const Text('로그아웃'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;

  const _StatCard({
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 8),
            Text(
              value,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}

class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _InfoTile({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey),
      title: Text(label),
      trailing: Text(
        value,
        style: const TextStyle(
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}

