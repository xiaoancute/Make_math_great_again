package com.makemathgreatagain

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawing
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.nio.charset.StandardCharsets

private const val PREFS = "math_learning"
private const val LEGACY_MASTERED_TOPICS = "mastered_topics"
private const val TOPIC_MEMORIES = "topic_memories"
private const val API_BASE_URL_PREF = "api_base_url"
private const val AI_MODEL_PREF = "ai_model"
private const val LEARNER_AGE_PREF = "learner_age"
private const val DEFAULT_LEARNER_AGE = 12
private const val PLACEMENT_PREF = "placement_result"
private const val DEFAULT_API_BASE_URL = "http://10.0.2.2:8000"
private const val OFFLINE_TOPICS_ASSET = "topics.json"
private const val DAY_MS = 24L * 60L * 60L * 1000L

private val MmgaColors = lightColorScheme(
    primary = Color(0xFF2F5EA8),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFE4EDFB),
    onPrimaryContainer = Color(0xFF163A6B),
    secondary = Color(0xFF0F7A66),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFD7F3EC),
    onSecondaryContainer = Color(0xFF0A4A3D),
    tertiary = Color(0xFFB35C00),
    tertiaryContainer = Color(0xFFFFE4C2),
    background = Color(0xFFF3F5F8),
    surface = Color.White,
    surfaceVariant = Color(0xFFE8ECF2),
    onSurface = Color(0xFF1A2230),
    onSurfaceVariant = Color(0xFF5A6474),
    outline = Color(0xFFD4DAE3),
    error = Color(0xFFB42318),
)

private val ScreenPad = 16.dp
private val CardR = RoundedCornerShape(16.dp)
private val PillR = RoundedCornerShape(999.dp)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent { MmgaApp() }
    }
}

private data class Topic(
    val id: String,
    val name: String,
    val gradeBand: String,
    val textbookPositions: List<TextbookPosition>,
    val human: String,
    val lifeExamples: List<String>,
    val why: String,
    val formalDefinition: String,
    val prerequisites: List<String>,
    val next: List<String>,
    val terms: Map<String, String>,
    val misconceptions: List<String>,
    val formulas: List<String>,
    val visuals: List<String>,
    val exerciseTypes: List<String>,
    val schoolRoute: List<String>,
    val route: List<String>,
    val conceptualLayers: List<String>,
    val workedExamples: List<WorkedExample>,
    val practiceLadder: List<PracticeTask>,
    val reflectionQuestions: List<String>,
)

private data class TextbookPosition(
    val curriculum: String,
    val grade: String,
    val chapter: String,
    val section: String,
)

private data class WorkedExample(
    val title: String,
    val problem: String,
    val steps: List<String>,
    val answerCheck: String,
)

private data class PracticeTask(
    val level: String,
    val prompt: String,
    val goal: String,
)

private data class ChatTurn(
    val question: String,
    val answer: String,
)

private data class TopicMemory(
    val topicId: String,
    val masteryLevel: Int,
    val firstSeenAt: Long,
    val lastReviewedAt: Long?,
    val nextReviewAt: Long?,
    val reviewCount: Int,
    val lapseCount: Int,
) {
    val isMastered: Boolean get() = masteryLevel >= 3
    fun isDue(now: Long): Boolean = isMastered && (nextReviewAt ?: 0L) <= now
}

private data class PlacementResult(
    val levelLabel: String,
    val levelRank: Int,
    val starterTopicId: String,
    val knownTopicIds: List<String>,
    val weakTopicIds: List<String>,
    val summary: String,
    val correctCount: Int,
    val totalCount: Int,
)

private data class DiagnosticItem(
    val id: String,
    val prompt: String,
    val choices: List<String>,
    val topicId: String,
    val correctIndex: Int,
)

private data class UiState(
    val loading: Boolean = true,
    val topics: List<Topic> = emptyList(),
    val selected: Topic? = null,
    val memories: Map<String, TopicMemory> = emptyMap(),
    val chat: List<ChatTurn> = emptyList(),
    val apiBaseUrl: String = DEFAULT_API_BASE_URL,
    val aiModel: String = "",
    val learnerAge: Int = DEFAULT_LEARNER_AGE,
    val aiStatus: String = "",
    val dataSource: String = "离线",
    val syncWarning: String? = null,
    val showSettings: Boolean = false,
    val placement: PlacementResult? = null,
    val showPlacement: Boolean = false,
) {
    val mastered: Set<String>
        get() = memories.values.filter { it.isMastered }.map { it.topicId }.toSet()
}

private data class GradeBucket(
    val key: String,
    val label: String,
    val topics: List<Topic>,
)

private enum class MainTab(val label: String) {
    Today("今天"),
    School("课本"),
    Review("温习"),
}

private enum class LessonStep(val title: String) {
    Intro("它是啥"),
    Why("为啥要学"),
    Example("举个例子"),
    Terms("几个词"),
    Worked("做一道"),
    Check("你会了吗"),
    Stuck("卡住了"),
}

@Composable
private fun MmgaApp() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val offlineTopics = remember { loadOfflineTopics(context) }
    val savedPlacement = remember { loadPlacement(context) }
    var state by remember {
        mutableStateOf(
            UiState(
                loading = false,
                topics = offlineTopics,
                memories = loadTopicMemories(context),
                apiBaseUrl = loadApiBaseUrl(context),
                aiModel = loadAiModel(context),
                learnerAge = loadLearnerAge(context),
                placement = savedPlacement,
                showPlacement = savedPlacement == null,
            ),
        )
    }

    suspend fun loadTopics(baseUrl: String = state.apiBaseUrl) {
        val selectedId = state.selected?.id
        val fallback = state.topics.ifEmpty { offlineTopics }
        state = state.copy(loading = true)
        state = try {
            val topics = fetchTopics(baseUrl)
            state.copy(
                loading = false,
                topics = topics,
                selected = selectedId?.let { id -> topics.firstOrNull { it.id == id } },
                dataSource = "联网",
                syncWarning = null,
            )
        } catch (error: Exception) {
            state.copy(
                loading = false,
                topics = fallback,
                selected = selectedId?.let { id -> fallback.firstOrNull { it.id == id } },
                dataSource = "离线",
                syncWarning = error.message ?: "现在连不上服务器",
            )
        }
    }

    LaunchedEffect(Unit) { loadTopics() }

    MaterialTheme(colorScheme = MmgaColors) {
        Surface(color = MaterialTheme.colorScheme.background) {
            AppScreen(
                state = state,
                onReload = { scope.launch { loadTopics() } },
                onSelect = { state = state.copy(selected = it, chat = emptyList(), showSettings = false) },
                onBack = {
                    when {
                        state.showPlacement && state.placement != null ->
                            state = state.copy(showPlacement = false)
                        state.showSettings ->
                            state = state.copy(showSettings = false)
                        else ->
                            state = state.copy(selected = null, chat = emptyList())
                    }
                },
                onOpenSettings = { state = state.copy(showSettings = true, selected = null) },
                onMarkUnderstood = { topic ->
                    val memories = state.memories.toMutableMap()
                    memories[topic.id] = memories[topic.id].markUnderstood(topic.id)
                    saveTopicMemories(context, memories)
                    state = state.copy(memories = memories)
                },
                onMarkNeedsWork = { topic ->
                    val memories = state.memories.toMutableMap()
                    memories[topic.id] = memories[topic.id].markOpen(topic.id)
                    saveTopicMemories(context, memories)
                    state = state.copy(memories = memories)
                },
                onAsk = { topic, question ->
                    val reply = try {
                        fetchTeacherAnswer(
                            state.apiBaseUrl,
                            topic.id,
                            question,
                            state.aiModel,
                            state.learnerAge,
                            state.mastered,
                            state.memories.values.toList(),
                            state.chat,
                            state.placement?.levelLabel,
                            state.placement?.summary,
                        )
                    } catch (_: Exception) {
                        if (state.chat.isEmpty()) {
                            offlineTeacherAnswer(
                                topic,
                                question,
                                state.topics,
                                state.mastered,
                                state.placement,
                            )
                        } else {
                            "现在联系不上在线老师，接不上刚才的对话。" +
                                "先照上面的讲解自查一轮，联网后接着问，会从你停下的地方继续。"
                        }
                    }
                    state = state.copy(chat = state.chat + ChatTurn(question, reply))
                },
                onSaveApiBaseUrl = { url ->
                    val normalized = normalizeBaseUrl(url)
                    saveApiBaseUrl(context, normalized)
                    state = state.copy(apiBaseUrl = normalized)
                    scope.launch { loadTopics(normalized) }
                },
                onSaveAiModel = { model ->
                    val normalized = model.trim()
                    saveAiModel(context, normalized)
                    state = state.copy(aiModel = normalized)
                },
                onSaveLearnerAge = { age ->
                    saveLearnerAge(context, age)
                    state = state.copy(learnerAge = age.coerceIn(6, 99))
                },
                onCheckAi = { url, model ->
                    val nUrl = normalizeBaseUrl(url)
                    val nModel = model.trim()
                    saveApiBaseUrl(context, nUrl)
                    saveAiModel(context, nModel)
                    state = state.copy(apiBaseUrl = nUrl, aiModel = nModel, aiStatus = "在连…")
                    scope.launch {
                        state = try {
                            state.copy(aiStatus = fetchAiStatus(nUrl, nModel))
                        } catch (_: Exception) {
                            state.copy(aiStatus = "连不上。没关系，离线也能学。")
                        }
                    }
                },
                onStartPlacement = {
                    state = state.copy(showPlacement = true, showSettings = false, selected = null)
                },
                onPlacementFinished = { result ->
                    savePlacement(context, result)
                    val memories = state.memories.toMutableMap()
                    val now = System.currentTimeMillis()
                    result.knownTopicIds.forEach { id ->
                        memories[id] = TopicMemory(
                            topicId = id,
                            masteryLevel = 3,
                            firstSeenAt = memories[id]?.firstSeenAt ?: now,
                            lastReviewedAt = now,
                            nextReviewAt = now + DAY_MS,
                            reviewCount = (memories[id]?.reviewCount ?: 0) + 1,
                            lapseCount = memories[id]?.lapseCount ?: 0,
                        )
                    }
                    result.weakTopicIds.forEach { id ->
                        if (id !in result.knownTopicIds) {
                            memories[id] = memories[id].markOpen(id)
                        }
                    }
                    saveTopicMemories(context, memories)
                    val starter = state.topics.firstOrNull { it.id == result.starterTopicId }
                    state = state.copy(
                        placement = result,
                        showPlacement = false,
                        memories = memories,
                        selected = starter,
                        chat = emptyList(),
                    )
                },
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun AppScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    onBack: () -> Unit,
    onOpenSettings: () -> Unit,
    onMarkUnderstood: (Topic) -> Unit,
    onMarkNeedsWork: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    onSaveApiBaseUrl: (String) -> Unit,
    onSaveAiModel: (String) -> Unit,
    onSaveLearnerAge: (Int) -> Unit,
    onCheckAi: (String, String) -> Unit,
    onStartPlacement: () -> Unit,
    onPlacementFinished: (PlacementResult) -> Unit,
) {
    var tab by rememberSaveable { mutableStateOf(MainTab.Today) }
    val inLesson = state.selected != null
    val inSettings = state.showSettings
    val inPlacement = state.showPlacement

    BackHandler(enabled = inLesson || inSettings, onBack = onBack)
    BackHandler(enabled = !inLesson && !inSettings && !inPlacement && tab != MainTab.Today) {
        tab = MainTab.Today
    }

    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        when {
                            inPlacement -> "摸底"
                            inSettings -> "设置"
                            inLesson -> "学这个"
                            else -> "数学"
                        },
                        fontWeight = FontWeight.SemiBold,
                    )
                },
                navigationIcon = {
                    if (inLesson || inSettings || (inPlacement && state.placement != null)) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.Filled.ArrowBack, contentDescription = "回去")
                        }
                    }
                },
                actions = {
                    if (!inLesson && !inSettings && !inPlacement) {
                        IconButton(onClick = onReload, enabled = !state.loading) {
                            Icon(Icons.Filled.Refresh, contentDescription = "刷新")
                        }
                        IconButton(onClick = onOpenSettings) {
                            Icon(Icons.Filled.Settings, contentDescription = "设置")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface,
                ),
            )
        },
        bottomBar = {
            if (!inLesson && !inSettings && !inPlacement) {
                NavigationBar(
                    containerColor = MaterialTheme.colorScheme.surface,
                    tonalElevation = 0.dp,
                ) {
                    MainTab.entries.forEach { item ->
                        NavigationBarItem(
                            selected = tab == item,
                            onClick = { tab = item },
                            icon = { TabDot(selected = tab == item) },
                            label = { Text(item.label) },
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = MaterialTheme.colorScheme.primary,
                                selectedTextColor = MaterialTheme.colorScheme.primary,
                                indicatorColor = MaterialTheme.colorScheme.primaryContainer,
                                unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant,
                            ),
                        )
                    }
                }
            }
        },
    ) { padding ->
        when {
            inPlacement -> PlacementScreen(
                apiBaseUrl = state.apiBaseUrl,
                onFinished = onPlacementFinished,
                modifier = Modifier.padding(padding),
            )
            inSettings -> SettingsScreen(
                state = state,
                onSaveApiBaseUrl = onSaveApiBaseUrl,
                onSaveAiModel = onSaveAiModel,
                onSaveLearnerAge = onSaveLearnerAge,
                onCheckAi = onCheckAi,
                onStartPlacement = onStartPlacement,
                modifier = Modifier.padding(padding),
            )
            inLesson -> LessonScreen(
                topic = state.selected!!,
                topics = state.topics,
                mastered = state.mastered,
                memories = state.memories,
                chat = state.chat,
                onMarkUnderstood = onMarkUnderstood,
                onMarkNeedsWork = onMarkNeedsWork,
                onAsk = onAsk,
                onSelectGap = onSelect,
                modifier = Modifier.padding(padding),
            )
            tab == MainTab.Today -> TodayScreen(
                state = state,
                onSelect = onSelect,
                onGoReview = { tab = MainTab.Review },
                onGoSchool = { tab = MainTab.School },
                modifier = Modifier.padding(padding),
            )
            tab == MainTab.School -> SchoolScreen(
                state = state,
                onSelect = onSelect,
                modifier = Modifier.padding(padding),
            )
            tab == MainTab.Review -> ReviewScreen(
                state = state,
                onSelect = onSelect,
                onMarkUnderstood = onMarkUnderstood,
                onMarkNeedsWork = onMarkNeedsWork,
                modifier = Modifier.padding(padding),
            )
        }
    }
}

@Composable
private fun TabDot(selected: Boolean) {
    Box(
        modifier = Modifier
            .size(10.dp)
            .clip(CircleShape)
            .background(
                if (selected) MaterialTheme.colorScheme.primary
                else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.35f),
            ),
    )
}

// region Today — learning home, not a catalog

@Composable
private fun TodayScreen(
    state: UiState,
    onSelect: (Topic) -> Unit,
    onGoReview: () -> Unit,
    onGoSchool: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val now = System.currentTimeMillis()
    val plan = remember(state.topics, state.mastered, state.memories, state.placement) {
        learningPlan(
            state.topics,
            state.mastered,
            state.memories,
            now,
            preferredStarterId = state.placement?.starterTopicId,
        )
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = ScreenPad, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        GreetingCard(
            mastered = state.mastered.size,
            total = state.topics.size,
            dueCount = plan.due.size,
            offline = state.dataSource == "离线",
            placementLabel = state.placement?.levelLabel,
            placementSummary = state.placement?.summary,
        )

        if (plan.due.isNotEmpty()) {
            ActionCard(
                eyebrow = "该温习一下了",
                title = plan.due.first().name,
                body = "以前会过，别让它又溜走。",
                primary = "温习一下",
                onPrimary = { onSelect(plan.due.first()) },
                secondary = if (plan.due.size > 1) "还有 ${plan.due.size - 1} 个" else null,
                onSecondary = onGoReview,
                accent = MaterialTheme.colorScheme.secondaryContainer,
            )
        }

        if (plan.next != null) {
            val weak = plan.next.prerequisites
                .filter { it !in state.mastered }
                .mapNotNull { id -> state.topics.firstOrNull { it.id == id } }
            ActionCard(
                eyebrow = "接着学这个",
                title = plan.next.name,
                body = plan.next.human.ifBlank { "别急着背，先搞清楚它在说啥。" },
                primary = "好，学这个",
                onPrimary = { onSelect(plan.next) },
                secondary = "我自己挑",
                onSecondary = onGoSchool,
                accent = MaterialTheme.colorScheme.primaryContainer,
            )
            if (weak.isNotEmpty()) {
                GapCard(
                    title = "前面有点空，先补一补",
                    topics = weak.take(3),
                    onSelect = onSelect,
                )
            }
        } else if (plan.due.isEmpty()) {
            SoftCard {
                Text("今天可以歇口气", fontWeight = FontWeight.SemiBold, fontSize = 18.sp)
                Body("想稳一点就去温习；想逛逛就从课本里挑。")
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(onClick = onGoReview, shape = CardR) { Text("温习") }
                    OutlinedButton(onClick = onGoSchool, shape = CardR) { Text("翻课本") }
                }
            }
        }

        if (plan.recentOpen.isNotEmpty()) {
            Text("上次没搞完", fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
            plan.recentOpen.take(4).forEach { topic ->
                MiniLessonRow(topic = topic, hint = "接着来") { onSelect(topic) }
            }
        }

        Spacer(Modifier.height(8.dp))
    }
}

@Composable
private fun GreetingCard(
    mastered: Int,
    total: Int,
    dueCount: Int,
    offline: Boolean,
    placementLabel: String? = null,
    placementSummary: String? = null,
) {
    SoftCard {
        Text(
            when {
                dueCount > 0 -> "先把旧的捡回来"
                mastered == 0 -> "从一小节开始就行"
                else -> "今天再往前挪一点"
            },
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
        )
        if (placementLabel != null) {
            Body("摸底大概在：$placementLabel")
        }
        Body(
            when {
                dueCount > 0 -> "有 $dueCount 个该温习了，新的先放一放。"
                mastered == 0 -> "不用一次学很多，弄懂一个算一个。"
                else -> "你已经弄懂 $mastered 个了，一共 $total 个。"
            },
        )
        if (!placementSummary.isNullOrBlank()) {
            Text(
                placementSummary,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 13.sp,
                lineHeight = 19.sp,
            )
        }
        if (offline) {
            Text(
                "没联网也没关系，照样能学",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 12.sp,
            )
        }
    }
}

@Composable
private fun ActionCard(
    eyebrow: String,
    title: String,
    body: String,
    primary: String,
    onPrimary: () -> Unit,
    secondary: String? = null,
    onSecondary: (() -> Unit)? = null,
    accent: Color,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardR,
        color = accent,
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                eyebrow,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 13.sp,
                fontWeight = FontWeight.Medium,
            )
            Text(title, fontSize = 24.sp, fontWeight = FontWeight.Bold, lineHeight = 30.sp)
            Body(body)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = onPrimary, shape = CardR) { Text(primary) }
                if (secondary != null && onSecondary != null) {
                    TextButton(onClick = onSecondary) { Text(secondary) }
                }
            }
        }
    }
}

@Composable
private fun GapCard(
    title: String,
    topics: List<Topic>,
    onSelect: (Topic) -> Unit,
) {
    SoftCard {
        Text(title, fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
        Body("前面空着，硬往下学容易懵。点一个补上。")
        topics.forEach { topic ->
            MiniLessonRow(topic = topic, hint = "补这个") { onSelect(topic) }
        }
    }
}

@Composable
private fun MiniLessonRow(
    topic: Topic,
    hint: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = CardR,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(topic.name, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(
                    topic.human,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    lineHeight = 18.sp,
                )
            }
            Text(hint, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Medium, fontSize = 13.sp)
        }
    }
}

// endregion

// region School — still a path, but lighter

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SchoolScreen(
    state: UiState,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    var query by rememberSaveable { mutableStateOf("") }
    var onlyOpen by rememberSaveable { mutableStateOf(false) }
    val buckets = remember(state.topics) { state.topics.schoolOrdered().gradeBuckets() }
    var gradeKey by rememberSaveable { mutableStateOf<String?>(null) }
    val selectedBucket = buckets.firstOrNull { it.key == gradeKey } ?: buckets.firstOrNull()
    val source = if (query.isBlank()) selectedBucket?.topics.orEmpty() else state.topics.schoolOrdered()
    val filtered = source.filter { topic ->
        val q = query.trim()
        val matchQ = q.isBlank() ||
            topic.name.contains(q, true) ||
            topic.human.contains(q, true) ||
            topic.schoolPlace().contains(q, true)
        val matchOpen = !onlyOpen || topic.id !in state.mastered
        matchQ && matchOpen
    }

    LaunchedEffect(buckets.map { it.key }.joinToString()) {
        if (buckets.isNotEmpty() && (gradeKey == null || buckets.none { it.key == gradeKey })) {
            gradeKey = buckets.first().key
        }
    }

    LazyColumn(
        modifier = modifier.fillMaxSize().padding(horizontal = ScreenPad),
        verticalArrangement = Arrangement.spacedBy(10.dp),
        contentPadding = PaddingValues(vertical = 8.dp),
    ) {
        item {
            Text("翻课本", fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Body("选年级，点开就学。")
        }
        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(buckets, key = { it.key }) { bucket ->
                    FilterChip(
                        selected = bucket.key == selectedBucket?.key && query.isBlank(),
                        onClick = {
                            gradeKey = bucket.key
                            query = ""
                        },
                        label = { Text(bucket.label) },
                    )
                }
            }
        }
        item {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("搜一搜，比如 分数") },
                leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
                shape = CardR,
            )
        }
        item {
            FilterChip(
                selected = onlyOpen,
                onClick = { onlyOpen = !onlyOpen },
                label = { Text(if (onlyOpen) "只看不会的" else "全都显示") },
            )
        }
        if (filtered.isEmpty()) {
            item { SoftCard { Body("没找到。换个词试试？") } }
        } else {
            items(filtered, key = { it.id }) { topic ->
                LessonListRow(
                    topic = topic,
                    mastered = topic.id in state.mastered,
                    subtitle = topic.schoolPlace(),
                    onClick = { onSelect(topic) },
                )
            }
        }
        item { Spacer(Modifier.height(8.dp)) }
    }
}

@Composable
private fun LessonListRow(
    topic: Topic,
    mastered: Boolean,
    subtitle: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = CardR,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(
                        if (mastered) MaterialTheme.colorScheme.secondaryContainer
                        else MaterialTheme.colorScheme.primaryContainer,
                    ),
                contentAlignment = Alignment.Center,
            ) {
                if (mastered) {
                    Icon(
                        Icons.Filled.Check,
                        contentDescription = "会了",
                        tint = MaterialTheme.colorScheme.secondary,
                        modifier = Modifier.size(20.dp),
                    )
                } else {
                    Text("看", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(topic.name, fontWeight = FontWeight.SemiBold, fontSize = 16.sp, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(
                    subtitle,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 12.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}

// endregion

// region Review

@Composable
private fun ReviewScreen(
    state: UiState,
    onSelect: (Topic) -> Unit,
    onMarkUnderstood: (Topic) -> Unit,
    onMarkNeedsWork: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val now = System.currentTimeMillis()
    val plan = remember(state.topics, state.mastered, state.memories) {
        learningPlan(state.topics, state.mastered, state.memories, now)
    }
    val focus = plan.due.firstOrNull()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPad),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        contentPadding = PaddingValues(vertical = 8.dp),
    ) {
        item {
            SoftCard {
                Text("温习", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                Body(
                    if (plan.due.isEmpty()) "今天没有该温习的。想学新的就回「今天」，或者随便翻一个。"
                    else "别急着点按钮。先想想：你还能自己讲出来吗？",
                )
            }
        }

        if (focus != null) {
            item {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shape = CardR,
                    color = MaterialTheme.colorScheme.secondaryContainer,
                ) {
                    Column(
                        modifier = Modifier.padding(18.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text(
                            "先看这个",
                            fontSize = 13.sp,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Text(focus.name, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                        Body(focus.human)
                        if (focus.reflectionQuestions.isNotEmpty()) {
                            Text(
                                "问自己一句：${focus.reflectionQuestions.first()}",
                                fontSize = 14.sp,
                                lineHeight = 20.sp,
                            )
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Button(
                                onClick = { onMarkUnderstood(focus) },
                                shape = CardR,
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = MaterialTheme.colorScheme.secondary,
                                ),
                            ) { Text("还记得") }
                            OutlinedButton(
                                onClick = { onMarkNeedsWork(focus) },
                                shape = CardR,
                            ) { Text("忘了") }
                            TextButton(onClick = { onSelect(focus) }) { Text("再看一遍") }
                        }
                    }
                }
            }
            if (plan.due.size > 1) {
                item {
                    Text("后面还有 ${plan.due.size - 1} 个", fontWeight = FontWeight.Medium)
                }
                items(plan.due.drop(1), key = { it.id }) { topic ->
                    MiniLessonRow(topic = topic, hint = "等等再看") { onSelect(topic) }
                }
            }
        } else {
            items(plan.masteredLater.take(12), key = { it.id }) { topic ->
                MiniLessonRow(topic = topic, hint = "再看看") { onSelect(topic) }
            }
        }
    }
}

// endregion

// region Lesson — the actual learning surface

@Composable
private fun LessonScreen(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    memories: Map<String, TopicMemory>,
    chat: List<ChatTurn>,
    onMarkUnderstood: (Topic) -> Unit,
    onMarkNeedsWork: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    onSelectGap: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val steps = remember(topic.id) { buildLessonSteps(topic) }
    var stepIndex by rememberSaveable(topic.id) { mutableIntStateOf(0) }
    val safeIndex = stepIndex.coerceIn(0, (steps.size - 1).coerceAtLeast(0))
    val step = steps.getOrNull(safeIndex)
    val progress = if (steps.isEmpty()) 0f else (safeIndex + 1f) / steps.size
    val weak = topic.prerequisites
        .filter { it !in mastered }
        .mapNotNull { id -> topics.firstOrNull { it.id == id } }

    Column(modifier = modifier.fillMaxSize()) {
        LinearProgressIndicator(
            progress = { progress },
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = ScreenPad),
        )
        Text(
            "${safeIndex + 1}/${steps.size.coerceAtLeast(1)}  ${step?.title.orEmpty()}",
            modifier = Modifier.padding(horizontal = ScreenPad, vertical = 8.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 13.sp,
        )

        Column(
            modifier = Modifier
                .weight(1f)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = ScreenPad),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Text(topic.name, fontSize = 26.sp, fontWeight = FontWeight.Bold, lineHeight = 32.sp)
            Text(
                topic.schoolPlace(),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 13.sp,
            )

            if (weak.isNotEmpty() && safeIndex == 0) {
                GapCard(title = "先把前面补上，再学这个", topics = weak.take(3), onSelect = onSelectGap)
            }

            when (step) {
                LessonStep.Intro -> LessonBlock {
                    BigLine(topic.human.ifBlank { "别背定义。你先说说，它大概在讲啥。" })
                    if (topic.route.isNotEmpty()) {
                        Body("可以按这个想：${topic.route.joinToString("，然后")}")
                    }
                }
                LessonStep.Why -> LessonBlock {
                    BigLine(topic.why.ifBlank { "它不是凭空冒出来的，是为了解决某个麻烦。" })
                    if (topic.formalDefinition.isNotBlank() && topic.formalDefinition != topic.human) {
                        Body("书上会写成：${topic.formalDefinition}")
                    }
                }
                LessonStep.Example -> LessonBlock {
                    if (topic.lifeExamples.isEmpty()) {
                        BigLine("想想生活里有没有差不多的事：数东西、分东西、比大小都行。")
                    } else {
                        topic.lifeExamples.forEachIndexed { i, ex ->
                            NumberedLine(i + 1, ex)
                        }
                    }
                    if (topic.visuals.isNotEmpty()) {
                        Body("画一画也行：${topic.visuals.joinToString("、")}")
                    }
                }
                LessonStep.Terms -> LessonBlock {
                    Body("先别急着背课名。下面这些词不懂，后面都会懵。")
                    if (topic.terms.isEmpty()) {
                        TermCard(
                            topic.name,
                            topic.human.ifBlank { "先问：这个词在题里指什么？" },
                        )
                    } else {
                        topic.terms.entries.forEach { (term, meaning) ->
                            TermCard(term, meaning)
                        }
                    }
                }
                LessonStep.Worked -> LessonBlock {
                    val examples = topic.workedExamples
                    if (examples.isEmpty()) {
                        BigLine("翻开课本找一道例题。先说清：知道什么、要求什么，再算。")
                        topic.practiceLadder.take(2).forEach { task ->
                            Body("${task.level}：${task.prompt}")
                        }
                    } else {
                        examples.take(2).forEach { ex ->
                            Text(ex.title, fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                            Body(ex.problem)
                            ex.steps.forEachIndexed { i, s -> NumberedLine(i + 1, s) }
                            if (ex.answerCheck.isNotBlank()) Body("做完看一眼：${ex.answerCheck}")
                            Spacer(Modifier.height(6.dp))
                        }
                    }
                    if (topic.misconceptions.isNotEmpty()) {
                        Body("很多人会栽在这：${topic.misconceptions.first()}")
                    }
                }
                LessonStep.Check -> LessonBlock {
                    val questions = topic.reflectionQuestions.ifEmpty {
                        listOf(
                            "不看书，你能说说它是啥吗？",
                            "能举个你自己的例子吗？",
                            "以后碰到什么题，会想到用它？",
                        )
                    }
                    questions.take(3).forEachIndexed { i, q -> NumberedLine(i + 1, q) }
                    Body("这几句都能答，再点下面的「会了」。答不上来也没关系，标「还不会」就行。")
                }
                LessonStep.Stuck -> StuckPanel(
                    topic = topic,
                    topics = topics,
                    mastered = mastered,
                    chat = chat,
                    onAsk = onAsk,
                )
                null -> SoftCard { Body("这节暂时没内容。") }
            }

            Spacer(Modifier.height(8.dp))
        }

        // Sticky lesson controls
        Surface(
            color = MaterialTheme.colorScheme.surface,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
            shadowElevation = 6.dp,
        ) {
            Column(
                modifier = Modifier.padding(ScreenPad),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    TextButton(
                        onClick = { stepIndex = (safeIndex - 1).coerceAtLeast(0) },
                        enabled = safeIndex > 0,
                    ) { Text("上一页") }
                    TextButton(
                        onClick = { stepIndex = (safeIndex + 1).coerceAtMost(steps.lastIndex) },
                        enabled = safeIndex < steps.lastIndex,
                    ) { Text("下一页") }
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    OutlinedButton(
                        onClick = { onMarkNeedsWork(topic) },
                        modifier = Modifier.weight(1f),
                        shape = CardR,
                    ) {
                        Icon(Icons.Filled.Close, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text(if (topic.id in mastered) "其实还不会" else "还不会")
                    }
                    Button(
                        onClick = { onMarkUnderstood(topic) },
                        modifier = Modifier.weight(1f),
                        shape = CardR,
                    ) {
                        Icon(Icons.Filled.Check, contentDescription = null, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(6.dp))
                        Text(if (topic.id in mastered) "温习过了" else "会了")
                    }
                }
                memories[topic.id]?.let { mem ->
                    Text(
                        mem.memoryLine(System.currentTimeMillis()),
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 12.sp,
                    )
                }
            }
        }
    }
}

@Composable
private fun LessonBlock(content: @Composable ColumnScope.() -> Unit) {
    SoftCard(content = content)
}

@Composable
private fun BigLine(text: String) {
    Text(text, fontSize = 18.sp, lineHeight = 28.sp, fontWeight = FontWeight.Medium)
}

@Composable
private fun NumberedLine(n: Int, text: String) {
    Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.Top) {
        Box(
            modifier = Modifier
                .size(26.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center,
        ) {
            Text("$n", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
        }
        Body(text, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun TermCard(term: String, meaning: String) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardR,
        color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.45f),
    ) {
        Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(term, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Body(meaning)
        }
    }
}

@Composable
private fun StuckPanel(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    chat: List<ChatTurn>,
    onAsk: suspend (Topic, String) -> Unit,
) {
    var question by rememberSaveable(topic.id) { mutableStateOf("") }
    var asking by remember(topic.id) { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val weak = topic.prerequisites.filter { it !in mastered }.names(topics)

    SoftCard {
        BigLine("卡在哪了？")
        Body("说清楚就行：哪个词不懂，还是哪一步算不动。答完还能接着追问，老师记得你们聊到哪了。")
        if (weak != "没有") {
            Body("我猜你可能还缺：$weak")
        }
        chat.forEach { turn ->
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = CardR,
                color = MaterialTheme.colorScheme.primaryContainer,
            ) {
                Text(
                    "你：${turn.question}",
                    modifier = Modifier.padding(12.dp),
                    fontSize = 14.sp,
                    lineHeight = 21.sp,
                )
            }
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = CardR,
                color = MaterialTheme.colorScheme.secondaryContainer,
            ) {
                Text(
                    turn.answer,
                    modifier = Modifier.padding(14.dp),
                    fontSize = 15.sp,
                    lineHeight = 23.sp,
                )
            }
        }
        if (chat.isEmpty()) {
            FlowRowQuickasks(topic) { q ->
                scope.launch {
                    asking = true
                    onAsk(topic, q)
                    asking = false
                }
            }
        }
        OutlinedTextField(
            value = question,
            onValueChange = { question = it },
            modifier = Modifier.fillMaxWidth(),
            minLines = 2,
            label = { Text(if (chat.isEmpty()) "把问题写在这儿" else "接着问，或写下你的想法") },
            enabled = !asking,
            shape = CardR,
        )
        Button(
            onClick = {
                val q = question.trim()
                if (q.isNotEmpty()) {
                    scope.launch {
                        asking = true
                        onAsk(topic, q)
                        question = ""
                        asking = false
                    }
                }
            },
            enabled = question.isNotBlank() && !asking,
            shape = CardR,
        ) {
            if (asking) {
                CircularProgressIndicator(
                    modifier = Modifier.size(16.dp),
                    color = MaterialTheme.colorScheme.onPrimary,
                    strokeWidth = 2.dp,
                )
                Spacer(Modifier.width(8.dp))
            }
            Text(if (chat.isEmpty()) "问问看" else "接着聊")
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun FlowRowQuickasks(topic: Topic, onPick: (String) -> Unit) {
    val asks = listOf(
        "${topic.name}到底是啥？",
        "为啥要学这个？",
        "举个生活里的例子呗",
    )
    FlowRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        asks.forEach { q ->
            FilterChip(selected = false, onClick = { onPick(q) }, label = { Text(q, maxLines = 1) })
        }
    }
}

// endregion

// region Settings

@Composable
private fun SettingsScreen(
    state: UiState,
    onSaveApiBaseUrl: (String) -> Unit,
    onSaveAiModel: (String) -> Unit,
    onSaveLearnerAge: (Int) -> Unit,
    onCheckAi: (String, String) -> Unit,
    onStartPlacement: () -> Unit,
    modifier: Modifier = Modifier,
) {
    var apiBaseUrl by rememberSaveable(state.apiBaseUrl) { mutableStateOf(state.apiBaseUrl) }
    var aiModel by rememberSaveable(state.aiModel) { mutableStateOf(state.aiModel) }
    var ageText by rememberSaveable(state.learnerAge) { mutableStateOf(state.learnerAge.toString()) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(ScreenPad),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        SoftCard {
            Text("连上网再问细一点", fontWeight = FontWeight.SemiBold, fontSize = 18.sp)
            Body("不设也行，离线就能学。接上之后，卡住能问得更细。")
            OutlinedTextField(
                value = apiBaseUrl,
                onValueChange = { apiBaseUrl = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("服务器地址") },
                shape = CardR,
            )
            OutlinedTextField(
                value = aiModel,
                onValueChange = { aiModel = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("用哪个模型") },
                shape = CardR,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(onClick = { onSaveApiBaseUrl(apiBaseUrl) }, shape = CardR) { Text("存一下") }
                OutlinedButton(onClick = { onCheckAi(apiBaseUrl, aiModel) }, shape = CardR) {
                    Text("试试连不连得上")
                }
            }
            if (aiModel.trim() != state.aiModel) {
                TextButton(onClick = { onSaveAiModel(aiModel) }) { Text("把模型名也存上") }
            }
            OutlinedTextField(
                value = ageText,
                onValueChange = { ageText = it.filter(Char::isDigit).take(2) },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("你的年龄（讲解会照这个调语气）") },
                shape = CardR,
            )
            val parsedAge = ageText.toIntOrNull()
            if (parsedAge != null && parsedAge in 6..99 && parsedAge != state.learnerAge) {
                TextButton(onClick = { onSaveLearnerAge(parsedAge) }) { Text("存一下年龄") }
            }
            if (state.aiStatus.isNotBlank()) Body(state.aiStatus)
            Body("现在是${state.dataSource}内容 · 你已经弄懂 ${state.mastered.size} 个")
            state.placement?.let { Body("摸底：${it.levelLabel}") }
            state.syncWarning?.let { Body(it) }
            Button(onClick = onStartPlacement, shape = CardR) { Text("重新摸底水平") }
        }
    }
}

// endregion


// region Placement — first-run level check

@Composable
private fun PlacementScreen(
    apiBaseUrl: String,
    onFinished: (PlacementResult) -> Unit,
    modifier: Modifier = Modifier,
) {
    val items = remember { offlineDiagnosticItems() }
    var index by rememberSaveable { mutableIntStateOf(0) }
    var answers by remember { mutableStateOf<Map<String, Int>>(emptyMap()) }
    var submitting by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    val item = items.getOrNull(index)

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(ScreenPad),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        SoftCard {
            Text("先摸个底", fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Body("不是考试。就想知道你卡在哪些词、哪些关系上。答完再开始讲。")
            Text(
                "${index + 1} / ${items.size}",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                fontSize = 13.sp,
            )
        }
        if (item != null) {
            SoftCard {
                BigLine(item.prompt)
                item.choices.forEachIndexed { choiceIndex, choice ->
                    val selected = answers[item.id] == choiceIndex
                    Surface(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                answers = answers + (item.id to choiceIndex)
                            },
                        shape = CardR,
                        color = if (selected) {
                            MaterialTheme.colorScheme.primaryContainer
                        } else {
                            MaterialTheme.colorScheme.surface
                        },
                        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                    ) {
                        Text(
                            choice,
                            modifier = Modifier.padding(14.dp),
                            fontSize = 15.sp,
                            lineHeight = 22.sp,
                        )
                    }
                }
            }
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                TextButton(
                    onClick = { index = (index - 1).coerceAtLeast(0) },
                    enabled = index > 0,
                ) { Text("上一题") }
                if (index < items.lastIndex) {
                    Button(
                        onClick = { index += 1 },
                        enabled = answers.containsKey(item.id),
                        shape = CardR,
                    ) { Text("下一题") }
                } else {
                    Button(
                        onClick = {
                            scope.launch {
                                submitting = true
                                error = null
                                try {
                                    val result = submitDiagnostic(
                                        apiBaseUrl,
                                        answers,
                                        items,
                                    )
                                    onFinished(result)
                                } catch (e: Exception) {
                                    error = e.message ?: "提交失败"
                                } finally {
                                    submitting = false
                                }
                            }
                        },
                        enabled = answers.size >= items.size && !submitting,
                        shape = CardR,
                    ) {
                        if (submitting) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp,
                                color = MaterialTheme.colorScheme.onPrimary,
                            )
                            Spacer(Modifier.width(8.dp))
                        }
                        Text("看结果")
                    }
                }
            }
        }
        error?.let { Body(it) }
    }
}

private fun offlineDiagnosticItems(): List<DiagnosticItem> = listOf(
    DiagnosticItem(
        id = "d_equality",
        prompt = "「等号 =」在说什么？",
        choices = listOf(
            "左边算完了，右边是答案",
            "左右两边表示同样多，像天平平衡",
            "一定要把数加起来",
            "只是写在竖式中间的符号",
        ),
        topicId = "equality",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_fraction",
        prompt = "把一个饼平均分成 4 块，拿走 1 块。这 1 块可以怎么说？",
        choices = listOf(
            "就是 1，因为拿走了一块",
            "是 1/4：把整体当成 1，这一块是其中一份",
            "是 4/1，因为一共 4 块",
            "分数只在做题时用，生活里不用",
        ),
        topicId = "fraction",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_quantity",
        prompt = "「小明比小红多 3 个苹果」这句话，核心在说什么？",
        choices = listOf(
            "只要会加减就能算，不用想关系",
            "两个量在比多少，差是 3",
            "一定要用乘法",
            "这是几何问题",
        ),
        topicId = "quantity_relationship",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_equation",
        prompt = "方程里的 x 是什么？",
        choices = listOf(
            "一个必须背下来的神秘字母",
            "暂时还不知道的量，用符号占个位置",
            "永远等于 0",
            "只能表示长度",
        ),
        topicId = "linear_equation_one_variable",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_transposition",
        prompt = "解方程时「移项要变号」，本质在干什么？",
        choices = listOf(
            "老师规定的口诀，背就行",
            "两边做同样的事，保持相等，只是写法变了",
            "把数字随便挪位置",
            "只有减法才能移项",
        ),
        topicId = "transposition",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_function",
        prompt = "「函数」这个词，最先该抓住哪一层意思？",
        choices = listOf(
            "一个很难的高中公式名",
            "一个量变了，另一个量按规则跟着变，且一个输入只对一个输出",
            "只要有 x 和 y 就是函数",
            "必须先会画很复杂的图像",
        ),
        topicId = "function_intro",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_set",
        prompt = "「集合」这个词，最先该抓住哪一层意思？",
        choices = listOf(
            "把一些确定的对象放在一起当成一个整体看，关键是说清「谁在里面、谁不在」",
            "就是一堆数字的另一种叫法",
            "必须写成花括号才算数学",
            "还没学过这个词，说不上来",
        ),
        topicId = "set_concept",
        correctIndex = 0,
    ),
    DiagnosticItem(
        id = "d_monotonic",
        prompt = "「函数单调递增」在描述什么关系？",
        choices = listOf(
            "图像必须是一条直线",
            "y 的值永远是正数",
            "在一段范围里，x 越大 y 跟着越大——两个量变化方向一致",
            "还没学过，说不上来",
        ),
        topicId = "function_properties_high_school",
        correctIndex = 2,
    ),
    DiagnosticItem(
        id = "d_sine",
        prompt = "「sin（正弦）」最先该抓住什么？",
        choices = listOf(
            "计算器上的一个按键，按了就有答案",
            "直角三角形里，锐角定了，对边与斜边的比也就定了——sin 说的就是这个比",
            "一串必须背下来的公式",
            "还没学过，说不上来",
        ),
        topicId = "trigonometric_functions",
        correctIndex = 1,
    ),
    DiagnosticItem(
        id = "d_derivative",
        prompt = "「导数」这个词，先抓哪一层意思？",
        choices = listOf(
            "一个套公式算出来的结果，意义不重要",
            "某一瞬间变化有多快——像车速表指针读数，不是全程平均速度",
            "和斜率没有关系的全新概念",
            "还没学过，说不上来",
        ),
        topicId = "derivative_intro",
        correctIndex = 1,
    ),
)

// Mirrors backend diagnostic.py — ids, ranks and names must stay in lockstep.
private val diagnosticRanks = mapOf(
    "equality" to 1,
    "fraction" to 2,
    "quantity_relationship" to 2,
    "linear_equation_one_variable" to 3,
    "transposition" to 3,
    "function_intro" to 4,
    "set_concept" to 5,
    "function_properties_high_school" to 5,
    "trigonometric_functions" to 6,
    "derivative_intro" to 6,
)

private val diagnosticNames = mapOf(
    "equality" to "等式",
    "fraction" to "分数",
    "quantity_relationship" to "数量关系",
    "linear_equation_one_variable" to "一元一次方程",
    "transposition" to "移项",
    "function_intro" to "函数入门",
    "set_concept" to "集合",
    "function_properties_high_school" to "函数性质",
    "trigonometric_functions" to "三角函数",
    "derivative_intro" to "导数入门",
)

private val diagnosticLevelLabels = mapOf(
    1 to "小学起步",
    2 to "小学中段",
    3 to "小初衔接",
    4 to "初中函数入门",
    5 to "高中入门",
    6 to "高中根基",
)

private fun scoreDiagnosticLocal(
    answers: Map<String, Int>,
    items: List<DiagnosticItem>,
): PlacementResult {
    val known = mutableListOf<String>()
    val wrong = mutableListOf<String>()
    var correct = 0
    val rankResults = sortedMapOf<Int, MutableList<Boolean>>()
    items.forEach { item ->
        val answered = answers[item.id] ?: return@forEach
        val ok = answered == item.correctIndex
        rankResults.getOrPut(diagnosticRanks[item.topicId] ?: 1) { mutableListOf() }.add(ok)
        if (ok) {
            correct += 1
            if (item.topicId !in known) known += item.topicId
        } else if (item.topicId !in wrong) {
            wrong += item.topicId
        }
    }
    // Climb rung by rung: a rank counts once every rank below is fully confirmed.
    var levelRank = 1
    var confirmed = 0
    for ((rank, results) in rankResults) {
        if (rank > confirmed + 1) break
        if (results.any { it }) levelRank = maxOf(levelRank, rank)
        if (!results.all { it }) break
        confirmed = rank
    }
    val levelLabel = diagnosticLevelLabels[levelRank] ?: "小学起步"
    // Only frontier misses are weak; a kid failing the derivative probe isn't "weak".
    val weak = wrong.filter { (diagnosticRanks[it] ?: 1) <= levelRank + 1 }
    val ladder = listOf(
        "equality",
        "fraction",
        "quantity_relationship",
        "linear_equation_one_variable",
        "transposition",
        "function_intro",
        "set_concept",
        "function_properties_high_school",
        "trigonometric_functions",
        "derivative_intro",
    )
    val starter = ladder.firstOrNull { it in weak }
        ?: ladder.firstOrNull { it !in known }
        ?: "derivative_intro"
    fun show(ids: List<String>) = ids.joinToString("、") { diagnosticNames[it] ?: it }
    val knownText = show(known).ifBlank { "还没确认会的" }
    val weakText = show(weak).ifBlank { "暂时没扫出大洞" }
    val starterText = diagnosticNames[starter] ?: starter
    val summary =
        "摸底结果：大约在「$levelLabel」。看起来比较稳的有：$knownText。" +
            "更该先补的是：$weakText。建议下一课从「$starterText」相关内容开始；" +
            "讲的时候仍会先拆词，不默认你会课本术语。"
    return PlacementResult(
        levelLabel = levelLabel,
        levelRank = levelRank,
        starterTopicId = starter,
        knownTopicIds = known,
        weakTopicIds = weak,
        summary = summary,
        correctCount = correct,
        totalCount = answers.size,
    )
}

private suspend fun submitDiagnostic(
    baseUrl: String,
    answers: Map<String, Int>,
    items: List<DiagnosticItem>,
): PlacementResult = withContext(Dispatchers.IO) {
    try {
        val array = JSONArray()
        answers.forEach { (id, choice) ->
            array.put(JSONObject().put("item_id", id).put("choice_index", choice))
        }
        val body = JSONObject().put("answers", array)
        val data = JSONObject(post(baseUrl, "/diagnostic/submit", body.toString()))
        PlacementResult(
            levelLabel = data.optString("level_label"),
            levelRank = data.optInt("level_rank"),
            starterTopicId = data.optString("starter_topic_id"),
            knownTopicIds = data.optJSONArray("known_topic_ids").toStringList(),
            weakTopicIds = data.optJSONArray("weak_topic_ids").toStringList(),
            summary = data.optString("summary"),
            correctCount = data.optInt("correct_count"),
            totalCount = data.optInt("total_count"),
        )
    } catch (_: Exception) {
        scoreDiagnosticLocal(answers, items)
    }
}

private fun loadPlacement(context: Context): PlacementResult? {
    val raw = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getString(PLACEMENT_PREF, null)
        ?: return null
    return try {
        val data = JSONObject(raw)
        PlacementResult(
            levelLabel = data.optString("level_label"),
            levelRank = data.optInt("level_rank"),
            starterTopicId = data.optString("starter_topic_id"),
            knownTopicIds = data.optJSONArray("known_topic_ids").toStringList(),
            weakTopicIds = data.optJSONArray("weak_topic_ids").toStringList(),
            summary = data.optString("summary"),
            correctCount = data.optInt("correct_count"),
            totalCount = data.optInt("total_count"),
        )
    } catch (_: Exception) {
        null
    }
}

private fun savePlacement(context: Context, value: PlacementResult) {
    val data = JSONObject()
        .put("level_label", value.levelLabel)
        .put("level_rank", value.levelRank)
        .put("starter_topic_id", value.starterTopicId)
        .put("known_topic_ids", JSONArray(value.knownTopicIds))
        .put("weak_topic_ids", JSONArray(value.weakTopicIds))
        .put("summary", value.summary)
        .put("correct_count", value.correctCount)
        .put("total_count", value.totalCount)
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putString(PLACEMENT_PREF, data.toString())
        .apply()
}

// endregion

// region Shared UI bits

@Composable
private fun SoftCard(
    modifier: Modifier = Modifier,
    content: @Composable ColumnScope.() -> Unit,
) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = CardR,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
            content = content,
        )
    }
}

@Composable
private fun Body(text: String, modifier: Modifier = Modifier) {
    Text(
        text,
        modifier = modifier,
        color = MaterialTheme.colorScheme.onSurface,
        fontSize = 15.sp,
        lineHeight = 23.sp,
    )
}

// endregion

// region Learning plan helpers

private data class LearningPlan(
    val next: Topic?,
    val due: List<Topic>,
    val recentOpen: List<Topic>,
    val masteredLater: List<Topic>,
)

private fun learningPlan(
    topics: List<Topic>,
    mastered: Set<String>,
    memories: Map<String, TopicMemory>,
    now: Long,
    preferredStarterId: String? = null,
): LearningPlan {
    val ordered = topics.understandingOrdered()
    val known = topics.map { it.id }.toSet()
    val open = ordered.filter { it.id !in mastered }
    val ready = open.filter { topic ->
        topic.prerequisites.filter { it in known }.all { it in mastered }
    }
    val preferred = preferredStarterId?.let { id -> open.firstOrNull { it.id == id } }
    val next = preferred ?: ready.firstOrNull() ?: open.firstOrNull()
    val masteredTopics = ordered.filter { it.id in mastered }
    val due = masteredTopics.filter { memories[it.id]?.isDue(now) == true }
    val later = masteredTopics.filter { it !in due }
    val recentOpen = open.filter { memories[it.id] != null && it.id != next?.id }
    return LearningPlan(next = next, due = due, recentOpen = recentOpen, masteredLater = later)
}

private fun buildLessonSteps(topic: Topic): List<LessonStep> {
    // Hard order: terms first, then what/why/example — never skip glossary.
    return listOf(
        LessonStep.Terms,
        LessonStep.Intro,
        LessonStep.Why,
        LessonStep.Example,
        LessonStep.Worked,
        LessonStep.Check,
        LessonStep.Stuck,
    )
}

private fun offlineTeacherAnswer(
    topic: Topic,
    question: String,
    topics: List<Topic>,
    mastered: Set<String>,
    placement: PlacementResult? = null,
): String {
    val weak = topic.prerequisites.filter { it !in mastered }.names(topics)
    return buildString {
        appendLine("你问的是：$question")
        if (placement != null) {
            appendLine()
            appendLine("摸底水平：${placement.levelLabel}")
            appendLine(placement.summary)
        } else {
            appendLine()
            appendLine("还没摸底：按你还不熟术语来讲。")
        }
        appendLine()
        appendLine("【先弄懂这些词】")
        if (topic.terms.isEmpty()) {
            appendLine("· ${topic.name}：${topic.human.ifBlank { "先问这个词在题里指什么" }}")
        } else {
            topic.terms.forEach { (k, v) -> appendLine("· $k：$v") }
        }
        appendLine()
        appendLine("【到底在讲什么】")
        appendLine(topic.human.ifBlank { "这节在讲一种数量或图形关系，别急着背名字。" })
        if (topic.why.isNotBlank()) {
            appendLine()
            appendLine("【为什么会出现】")
            appendLine(topic.why)
        }
        if (topic.lifeExamples.isNotEmpty()) {
            appendLine()
            appendLine("【举个例子】")
            appendLine(topic.lifeExamples.joinToString("；"))
        }
        if (topic.formalDefinition.isNotBlank() && topic.formalDefinition != topic.human) {
            appendLine()
            appendLine("【课本会怎么说】")
            appendLine(topic.formalDefinition)
        }
        if (weak != "没有") {
            appendLine()
            appendLine("你要是觉得懵，多半是前面还缺：$weak")
        }
        appendLine()
        appendLine("（没联网，先按本地这样讲。想问更细，去设置里接服务器。）")
    }.trim()
}

// endregion

// region Ordering / labels (kept from previous shell)

private fun List<String>.names(
    topics: List<Topic>,
    onlyMastered: Set<String>? = null,
    excludeMastered: Set<String>? = null,
): String {
    val names = filter {
        (onlyMastered == null || it in onlyMastered) &&
            (excludeMastered == null || it !in excludeMastered)
    }.map { id -> topics.firstOrNull { it.id == id }?.name ?: id }
    return names.joinToString("、").ifBlank { "没有" }
}

private fun Topic.schoolPlace(): String {
    val position = textbookPositions.firstOrNull()
    if (position != null) {
        return listOf(position.grade, position.chapter, position.section)
            .filter { it.isNotBlank() }
            .joinToString(" · ")
            .ifBlank { stageLabel() }
    }
    return schoolRoute.joinToString(" · ").ifBlank { stageLabel() }
}

private fun Topic.stageLabel(): String = when (gradeBand) {
    "primary" -> "小学"
    "junior" -> "初中"
    "primary_to_junior" -> "小初衔接"
    "senior" -> "高中"
    else -> gradeBand.ifBlank { "校内" }
}

private fun List<Topic>.schoolOrdered(): List<Topic> = mapIndexed { index, topic -> index to topic }
    .sortedWith(
        compareBy<Pair<Int, Topic>> { it.second.textbookPositions.firstOrNull()?.grade.gradeOrder() }
            .thenBy { it.second.textbookPositions.firstOrNull()?.chapter.chapterOrder() }
            .thenBy { it.first },
    )
    .map { it.second }

private fun List<Topic>.gradeBuckets(): List<GradeBucket> {
    val order = listOf(
        "一年级", "二年级", "三年级", "四年级", "五年级", "六年级",
        "七年级", "八年级", "九年级", "高一", "高二", "高三",
        "小学", "初中", "高中", "其他",
    )
    val grouped = groupBy { it.schoolGradeKey() }
    return order.mapNotNull { key ->
        grouped[key]?.let { GradeBucket(key = key, label = key, topics = it) }
    }
}

private fun Topic.schoolGradeKey(): String {
    val value = textbookPositions.firstOrNull()?.grade.orEmpty()
    return when {
        "一年级" in value -> "一年级"
        "二年级" in value -> "二年级"
        "三年级" in value -> "三年级"
        "四年级" in value -> "四年级"
        "五年级" in value -> "五年级"
        "六年级" in value -> "六年级"
        "七年级" in value -> "七年级"
        "八年级" in value -> "八年级"
        "九年级" in value -> "九年级"
        "高中必修第一册" in value -> "高一"
        "高中必修第二册" in value -> "高一"
        "高中选择性必修第一册" in value -> "高二"
        "高中选择性必修第二册" in value -> "高二"
        "高中选择性必修第三册" in value -> "高三"
        "高中" in value -> "高中"
        gradeBand == "primary" -> "小学"
        gradeBand == "junior" -> "初中"
        gradeBand == "senior" -> "高中"
        else -> "其他"
    }
}

private fun List<Topic>.understandingOrdered(): List<Topic> {
    val schoolOrder = schoolOrdered()
    val byId = schoolOrder.associateBy { it.id }
    val unresolved = schoolOrder.associate { it.id to it.prerequisites.count { id -> id in byId } }
        .toMutableMap()
    val dependents = mutableMapOf<String, MutableList<String>>()
    schoolOrder.forEach { topic ->
        topic.prerequisites.filter { it in byId }.forEach { prerequisite ->
            dependents.getOrPut(prerequisite) { mutableListOf() }.add(topic.id)
        }
    }
    val queue = schoolOrder.filter { unresolved[it.id] == 0 }.map { it.id }.toMutableList()
    val result = mutableListOf<Topic>()
    while (queue.isNotEmpty()) {
        val id = queue.removeAt(0)
        val topic = byId[id] ?: continue
        if (result.any { it.id == id }) continue
        result += topic
        dependents[id].orEmpty().forEach { nextId ->
            val nextCount = (unresolved[nextId] ?: 0) - 1
            unresolved[nextId] = nextCount
            if (nextCount == 0) queue += nextId
        }
    }
    if (result.size == schoolOrder.size) return result
    val seen = result.map { it.id }.toSet()
    return result + schoolOrder.filter { it.id !in seen }
}

private fun String?.gradeOrder(): Int {
    val value = this.orEmpty()
    val grade = when {
        "一年级" in value -> 1
        "二年级" in value -> 2
        "三年级" in value -> 3
        "四年级" in value -> 4
        "五年级" in value -> 5
        "六年级" in value -> 6
        "七年级" in value -> 7
        "八年级" in value -> 8
        "九年级" in value -> 9
        "高中必修第一册" in value -> 10
        "高中必修第二册" in value -> 11
        "高中选择性必修第一册" in value -> 12
        "高中选择性必修第二册" in value -> 13
        "高中选择性必修第三册" in value -> 14
        "高中" in value -> 10
        "小学" in value -> 3
        "初中" in value -> 7
        else -> 99
    }
    val volume = when {
        "上册" in value -> 0
        "下册" in value -> 1
        else -> 0
    }
    return grade * 10 + volume
}

private fun String?.chapterOrder(): Int {
    val value = this.orEmpty()
    val chineseDigits = mapOf(
        '一' to 1, '二' to 2, '三' to 3, '四' to 4, '五' to 5,
        '六' to 6, '七' to 7, '八' to 8, '九' to 9, '十' to 10,
    )
    Regex("""第(\d+)章""").find(value)?.groupValues?.get(1)?.toIntOrNull()?.let { return it }
    Regex("""第([一二三四五六七八九十]+)章""").find(value)?.groupValues?.get(1)?.let { text ->
        if (text == "十") return 10
        if (text.length == 1) return chineseDigits[text.first()] ?: 99
        if (text.startsWith("十")) return 10 + (chineseDigits[text.last()] ?: 0)
        if (text.endsWith("十")) return (chineseDigits[text.first()] ?: 0) * 10
        return (chineseDigits[text.first()] ?: 0) * 10 + (chineseDigits[text.last()] ?: 0)
    }
    return 99
}

// endregion

// region Persistence / network (unchanged contracts)

private fun loadOfflineTopics(context: Context): List<Topic> =
    try {
        context.assets.open(OFFLINE_TOPICS_ASSET).bufferedReader(StandardCharsets.UTF_8).use {
            JSONArray(it.readText()).toTopics()
        }
    } catch (_: Exception) {
        emptyList()
    }

private suspend fun fetchTopics(baseUrl: String): List<Topic> = withContext(Dispatchers.IO) {
    JSONArray(fetch(baseUrl, "/topics")).toTopics()
}

private suspend fun fetchTeacherAnswer(
    baseUrl: String,
    topicId: String,
    question: String,
    model: String,
    learnerAge: Int,
    mastered: Set<String>,
    memories: List<TopicMemory>,
    history: List<ChatTurn>,
    placementLevel: String? = null,
    placementSummary: String? = null,
): String = withContext(Dispatchers.IO) {
    val historyArray = JSONArray()
    history.forEach { turn ->
        historyArray.put(
            JSONObject().put("question", turn.question).put("answer", turn.answer),
        )
    }
    val body = JSONObject()
        .put("age", learnerAge.coerceIn(6, 99))
        .put("question", question)
        .put("model", model.trim())
        .put("mastered", JSONArray(mastered.sorted()))
        .put("memories", memories.sortedBy { it.topicId }.toRequestJsonArray())
        .put("history", historyArray)
        .put("placement_level", placementLevel ?: JSONObject.NULL)
        .put("placement_summary", placementSummary ?: JSONObject.NULL)
    val data = JSONObject(post(baseUrl, "/topics/$topicId/teacher-answer", body.toString()))
    val answer = data.optString("answer")
    if (data.optString("source") == "local") "【离线讲解】\n$answer" else answer
}

private suspend fun fetchAiStatus(baseUrl: String, model: String): String =
    withContext(Dispatchers.IO) {
        val body = JSONObject().put("model", model.trim())
        val data = JSONObject(post(baseUrl, "/ai/status", body.toString()))
        val backendOk = data.optString("backend") == "ok"
        val hasKey = data.optBoolean("openai_key_configured")
        val hasModel = data.optBoolean("model_configured")
        val selectedModel = data.optString("model")
        when {
            !backendOk -> "服务器有点不对"
            !hasKey -> "服务器还没配好钥匙（OPENAI_API_KEY）"
            !hasModel -> "模型名还空着"
            else -> "连上了，用的是 $selectedModel"
        }
    }

private fun JSONArray.toTopics(): List<Topic> =
    List(length()) { index -> getJSONObject(index).toTopic() }

private fun JSONObject.toTopic(): Topic = Topic(
    id = optString("id"),
    name = optString("name"),
    gradeBand = optString("grade_band"),
    textbookPositions = optJSONArray("textbook_positions").toTextbookPositions(),
    human = optString("human_explanation"),
    lifeExamples = optJSONArray("life_examples").toStringList(),
    why = optString("why_needed"),
    formalDefinition = optString("formal_definition"),
    prerequisites = optJSONArray("prerequisite_ids").toStringList(),
    next = optJSONArray("next_ids").toStringList(),
    terms = optJSONObject("term_explanations").toStringMap(),
    misconceptions = optJSONArray("misconceptions").toStringList(),
    formulas = optJSONArray("formulas").toStringList(),
    visuals = optJSONArray("visualization_methods").toStringList(),
    exerciseTypes = optJSONArray("exercise_types").toStringList(),
    schoolRoute = optJSONArray("school_route").toStringList(),
    route = optJSONArray("understanding_route").toStringList(),
    conceptualLayers = optJSONArray("conceptual_layers").toStringList(),
    workedExamples = optJSONArray("worked_examples").toWorkedExamples(),
    practiceLadder = optJSONArray("practice_ladder").toPracticeTasks(),
    reflectionQuestions = optJSONArray("reflection_questions").toStringList(),
)

private fun JSONArray?.toTextbookPositions(): List<TextbookPosition> {
    if (this == null) return emptyList()
    return List(length()) { index ->
        val item = optJSONObject(index) ?: JSONObject()
        TextbookPosition(
            curriculum = item.optString("curriculum"),
            grade = item.optString("grade"),
            chapter = item.optString("chapter"),
            section = item.optString("section"),
        )
    }
}

private fun JSONArray?.toStringList(): List<String> {
    if (this == null) return emptyList()
    return List(length()) { index -> optString(index) }
}

private fun JSONArray?.toWorkedExamples(): List<WorkedExample> {
    if (this == null) return emptyList()
    return List(length()) { index ->
        val item = optJSONObject(index) ?: JSONObject()
        WorkedExample(
            title = item.optString("title"),
            problem = item.optString("problem"),
            steps = item.optJSONArray("steps").toStringList(),
            answerCheck = item.optString("answer_check"),
        )
    }
}

private fun JSONArray?.toPracticeTasks(): List<PracticeTask> {
    if (this == null) return emptyList()
    return List(length()) { index ->
        val item = optJSONObject(index) ?: JSONObject()
        PracticeTask(
            level = item.optString("level"),
            prompt = item.optString("prompt"),
            goal = item.optString("goal"),
        )
    }
}

private fun JSONObject?.toStringMap(): Map<String, String> {
    if (this == null) return emptyMap()
    return keys().asSequence().associateWith { key -> optString(key) }
}

private fun loadTopicMemories(context: Context): Map<String, TopicMemory> {
    val prefs = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
    val saved = prefs.getString(TOPIC_MEMORIES, null)
    val parsed = saved?.let { value ->
        try {
            JSONArray(value).toTopicMemories()
        } catch (_: Exception) {
            emptyMap()
        }
    }.orEmpty()
    if (parsed.isNotEmpty()) return parsed

    val legacy = prefs.getStringSet(LEGACY_MASTERED_TOPICS, emptySet()).orEmpty()
    if (legacy.isEmpty()) return emptyMap()

    val now = System.currentTimeMillis()
    val migrated = legacy.associateWith { topicId ->
        TopicMemory(
            topicId = topicId,
            masteryLevel = 3,
            firstSeenAt = now,
            lastReviewedAt = now,
            nextReviewAt = now + DAY_MS,
            reviewCount = 1,
            lapseCount = 0,
        )
    }
    saveTopicMemories(context, migrated)
    return migrated
}

private fun saveTopicMemories(context: Context, value: Map<String, TopicMemory>) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putString(TOPIC_MEMORIES, value.values.sortedBy { it.topicId }.toJsonArray().toString())
        .apply()
}

private fun JSONArray.toTopicMemories(): Map<String, TopicMemory> =
    List(length()) { index -> optJSONObject(index) }
        .filterNotNull()
        .mapNotNull { item -> item.toTopicMemory() }
        .associateBy { it.topicId }

private fun JSONObject.toTopicMemory(): TopicMemory? {
    val topicId = optString("topic_id").ifBlank { optString("topicId") }
    if (topicId.isBlank()) return null
    return TopicMemory(
        topicId = topicId,
        masteryLevel = optInt("mastery_level", optInt("masteryLevel", 0)).coerceIn(0, 5),
        firstSeenAt = optLong("first_seen_at", optLong("firstSeenAt", System.currentTimeMillis())),
        lastReviewedAt = optNullableLong("last_reviewed_at", "lastReviewedAt"),
        nextReviewAt = optNullableLong("next_review_at", "nextReviewAt"),
        reviewCount = optInt("review_count", optInt("reviewCount", 0)).coerceAtLeast(0),
        lapseCount = optInt("lapse_count", optInt("lapseCount", 0)).coerceAtLeast(0),
    )
}

private fun JSONObject.optNullableLong(primary: String, fallback: String): Long? {
    val key = when {
        has(primary) && !isNull(primary) -> primary
        has(fallback) && !isNull(fallback) -> fallback
        else -> return null
    }
    return optLong(key)
}

private fun Collection<TopicMemory>.toJsonArray(): JSONArray {
    val array = JSONArray()
    forEach { memory ->
        array.put(
            JSONObject()
                .put("topic_id", memory.topicId)
                .put("mastery_level", memory.masteryLevel)
                .put("first_seen_at", memory.firstSeenAt)
                .put("last_reviewed_at", memory.lastReviewedAt)
                .put("next_review_at", memory.nextReviewAt)
                .put("review_count", memory.reviewCount)
                .put("lapse_count", memory.lapseCount),
        )
    }
    return array
}

private fun Collection<TopicMemory>.toRequestJsonArray(): JSONArray {
    val array = JSONArray()
    forEach { memory ->
        array.put(
            JSONObject()
                .put("topic_id", memory.topicId)
                .put("mastery_level", memory.masteryLevel)
                .put("last_reviewed_at", memory.lastReviewedAt)
                .put("next_review_at", memory.nextReviewAt)
                .put("review_count", memory.reviewCount)
                .put("lapse_count", memory.lapseCount),
        )
    }
    return array
}

private fun TopicMemory?.markUnderstood(topicId: String): TopicMemory {
    val now = System.currentTimeMillis()
    val previous = this
    val reviewCount = (previous?.reviewCount ?: 0) + 1
    return TopicMemory(
        topicId = topicId,
        masteryLevel = 3,
        firstSeenAt = previous?.firstSeenAt ?: now,
        lastReviewedAt = now,
        nextReviewAt = now + nextReviewDelay(reviewCount),
        reviewCount = reviewCount,
        lapseCount = previous?.lapseCount ?: 0,
    )
}

private fun TopicMemory?.markOpen(topicId: String): TopicMemory {
    val now = System.currentTimeMillis()
    val previous = this
    return TopicMemory(
        topicId = topicId,
        masteryLevel = 1,
        firstSeenAt = previous?.firstSeenAt ?: now,
        lastReviewedAt = now,
        nextReviewAt = now + DAY_MS,
        reviewCount = previous?.reviewCount ?: 0,
        lapseCount = (previous?.lapseCount ?: 0) + 1,
    )
}

private fun nextReviewDelay(reviewCount: Int): Long =
    when (reviewCount) {
        0, 1 -> DAY_MS
        2 -> 3L * DAY_MS
        else -> 7L * DAY_MS
    }

private fun TopicMemory.memoryLine(now: Long): String {
    if (!isMastered) return "这节你还没站稳，过两天再碰一碰。"
    val due = nextReviewAt ?: return "先记着，过几天再温习。"
    val remaining = due - now
    val days = ((remaining + DAY_MS - 1) / DAY_MS).toInt()
    return when {
        remaining <= 0 -> "该再看一眼了（你已经温习过 $reviewCount 次）"
        days <= 1 -> "差不多明天再温习"
        else -> "大概 $days 天后再温习"
    }
}

private fun loadApiBaseUrl(context: Context): String =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getString(API_BASE_URL_PREF, DEFAULT_API_BASE_URL)
        .orEmpty()
        .ifBlank { DEFAULT_API_BASE_URL }

private fun saveApiBaseUrl(context: Context, value: String) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putString(API_BASE_URL_PREF, value)
        .apply()
}

private fun loadAiModel(context: Context): String =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getString(AI_MODEL_PREF, "")
        .orEmpty()

private fun saveAiModel(context: Context, value: String) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putString(AI_MODEL_PREF, value)
        .apply()
}

private fun loadLearnerAge(context: Context): Int =
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .getInt(LEARNER_AGE_PREF, DEFAULT_LEARNER_AGE)
        .coerceIn(6, 99)

private fun saveLearnerAge(context: Context, value: Int) {
    context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
        .edit()
        .putInt(LEARNER_AGE_PREF, value.coerceIn(6, 99))
        .apply()
}

private fun normalizeBaseUrl(value: String): String =
    value.trim().trimEnd('/').ifBlank { DEFAULT_API_BASE_URL }

private fun fetch(baseUrl: String, path: String): String {
    val connection = URL(normalizeBaseUrl(baseUrl) + path).openConnection() as HttpURLConnection
    return try {
        connection.connectTimeout = 3000
        connection.readTimeout = 3000
        connection.requestMethod = "GET"
        if (connection.responseCode >= 400) error("HTTP ${connection.responseCode}")
        connection.inputStream.bufferedReader().use { it.readText() }
    } finally {
        connection.disconnect()
    }
}

private fun post(baseUrl: String, path: String, body: String): String {
    val connection = URL(normalizeBaseUrl(baseUrl) + path).openConnection() as HttpURLConnection
    return try {
        connection.connectTimeout = 3000
        connection.readTimeout = 20000
        connection.requestMethod = "POST"
        connection.doOutput = true
        connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
        connection.outputStream.use { output ->
            output.write(body.toByteArray(StandardCharsets.UTF_8))
        }
        if (connection.responseCode >= 400) error("HTTP ${connection.responseCode}")
        connection.inputStream.bufferedReader().use { it.readText() }
    } finally {
        connection.disconnect()
    }
}

// endregion
