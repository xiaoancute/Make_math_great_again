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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
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
private const val DEFAULT_API_BASE_URL = "http://10.0.2.2:8000"
private const val OFFLINE_TOPICS_ASSET = "topics.json"
private const val DAY_MS = 24L * 60L * 60L * 1000L

private val MmgaColors = lightColorScheme(
    primary = Color(0xFF315CA8),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFE7EEF9),
    onPrimaryContainer = Color(0xFF173765),
    secondary = Color(0xFF17756B),
    secondaryContainer = Color(0xFFE1F3EF),
    tertiary = Color(0xFF9A5B10),
    tertiaryContainer = Color(0xFFFFE9C2),
    background = Color(0xFFF5F6F8),
    surface = Color.White,
    surfaceVariant = Color(0xFFE7EAF0),
    onSurface = Color(0xFF1D2430),
    onSurfaceVariant = Color(0xFF5C6472),
    outline = Color(0xFFD6DAE2),
    error = Color(0xFFB42318),
)

private val ScreenPadding = 18.dp
private val CardShape = RoundedCornerShape(8.dp)
private val PillShape = RoundedCornerShape(999.dp)

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

private data class TopicMemory(
    val topicId: String,
    val masteryLevel: Int,
    val firstSeenAt: Long,
    val lastReviewedAt: Long?,
    val nextReviewAt: Long?,
    val reviewCount: Int,
    val lapseCount: Int,
) {
    val isMastered: Boolean
        get() = masteryLevel >= 3

    fun isDue(now: Long): Boolean = isMastered && (nextReviewAt ?: 0L) <= now
}

private data class UiState(
    val loading: Boolean = true,
    val error: String? = null,
    val topics: List<Topic> = emptyList(),
    val selected: Topic? = null,
    val memories: Map<String, TopicMemory> = emptyMap(),
    val answer: String = "",
    val apiBaseUrl: String = DEFAULT_API_BASE_URL,
    val aiModel: String = "",
    val aiStatus: String = "",
    val dataSource: String = "本机离线",
    val syncWarning: String? = null,
) {
    val mastered: Set<String>
        get() = memories.values.filter { it.isMastered }.map { it.topicId }.toSet()
}

private data class GradeBucket(
    val key: String,
    val label: String,
    val topics: List<Topic>,
)

private enum class TopicFilter(val label: String) {
    All("全部"),
    Open("还没懂"),
    Mastered("已经懂"),
}

private enum class MainTab(val label: String) {
    School("校内"),
    Understand("理解"),
    Review("复习"),
    Settings("设置"),
}

@Composable
private fun MmgaApp() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val offlineTopics = remember { loadOfflineTopics(context) }
    var state by remember {
        mutableStateOf(
            UiState(
                loading = false,
                topics = offlineTopics,
                memories = loadTopicMemories(context),
                apiBaseUrl = loadApiBaseUrl(context),
                aiModel = loadAiModel(context),
            ),
        )
    }

    suspend fun loadTopics(baseUrl: String = state.apiBaseUrl) {
        val selectedId = state.selected?.id
        val fallbackTopics = state.topics.ifEmpty { offlineTopics }
        state = state.copy(loading = true, error = null)
        state = try {
            val topics = fetchTopics(baseUrl)
            state.copy(
                loading = false,
                topics = topics,
                selected = selectedId?.let { id -> topics.firstOrNull { it.id == id } },
                error = null,
                dataSource = "后端同步",
                syncWarning = null,
            )
        } catch (error: Exception) {
            state.copy(
                loading = false,
                topics = fallbackTopics,
                selected = selectedId?.let { id ->
                    fallbackTopics.firstOrNull { it.id == id }
                },
                error = null,
                dataSource = "本机离线",
                syncWarning = error.message ?: "后端暂时不可用",
            )
        }
    }

    LaunchedEffect(Unit) {
        loadTopics()
    }

    MaterialTheme(colorScheme = MmgaColors) {
        Surface(color = MaterialTheme.colorScheme.background) {
            AppScreen(
                state = state,
                onReload = { scope.launch { loadTopics() } },
                onSelect = { state = state.copy(selected = it, answer = "") },
                onBack = { state = state.copy(selected = null, answer = "") },
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
                    state = state.copy(answer = "AI 老师正在根据掌握记录回答")
                    state = try {
                        state.copy(
                            answer = fetchTeacherAnswer(
                                state.apiBaseUrl,
                                topic.id,
                                question,
                                state.aiModel,
                                state.mastered,
                                state.memories.values.toList(),
                            ),
                        )
                    } catch (_: Exception) {
                        state.copy(
                            answer = "AI 后端未连接。校内内容可以继续看；"
                                + "设置里填可访问的后端地址后再问。",
                        )
                    }
                },
                onSaveApiBaseUrl = { apiBaseUrl ->
                    val normalized = normalizeBaseUrl(apiBaseUrl)
                    saveApiBaseUrl(context, normalized)
                    state = state.copy(apiBaseUrl = normalized)
                    scope.launch { loadTopics(normalized) }
                },
                onSaveAiModel = { model ->
                    val normalized = model.trim()
                    saveAiModel(context, normalized)
                    state = state.copy(aiModel = normalized)
                },
                onCheckAi = { apiBaseUrl, model ->
                    val normalizedUrl = normalizeBaseUrl(apiBaseUrl)
                    val normalizedModel = model.trim()
                    saveApiBaseUrl(context, normalizedUrl)
                    saveAiModel(context, normalizedModel)
                    state = state.copy(
                        apiBaseUrl = normalizedUrl,
                        aiModel = normalizedModel,
                        aiStatus = "正在测试连接",
                    )
                    scope.launch {
                        state = try {
                            state.copy(aiStatus = fetchAiStatus(normalizedUrl, normalizedModel))
                        } catch (_: Exception) {
                            state.copy(aiStatus = "后端不可达")
                        }
                    }
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
    onMarkUnderstood: (Topic) -> Unit,
    onMarkNeedsWork: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    onSaveApiBaseUrl: (String) -> Unit,
    onSaveAiModel: (String) -> Unit,
    onCheckAi: (String, String) -> Unit,
) {
    var selectedTab by rememberSaveable { mutableStateOf(MainTab.School) }

    BackHandler(enabled = state.selected != null, onBack = onBack)
    BackHandler(enabled = state.selected == null && selectedTab != MainTab.School) {
        selectedTab = MainTab.School
    }

    Scaffold(
        contentWindowInsets = WindowInsets.safeDrawing,
        topBar = {
            TopAppBar(
                title = { Text("MMGA", fontWeight = FontWeight.SemiBold) },
                navigationIcon = {
                    if (state.selected != null) {
                        IconButton(onClick = onBack) {
                            Icon(Icons.Filled.ArrowBack, contentDescription = "返回")
                        }
                    }
                },
                actions = {
                    IconButton(onClick = onReload, enabled = !state.loading) {
                        Icon(Icons.Filled.Refresh, contentDescription = "刷新")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                    navigationIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                ),
            )
        },
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 0.dp,
            ) {
                MainTab.entries.forEach { tab ->
                    NavigationBarItem(
                        selected = selectedTab == tab && state.selected == null,
                        onClick = {
                            if (state.selected != null) onBack()
                            selectedTab = tab
                        },
                        icon = { TabIcon(tab) },
                        label = { Text(tab.label) },
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
        },
    ) { padding ->
        if (state.selected != null) {
            TopicDetail(
                topic = state.selected,
                topics = state.topics,
                mastered = state.mastered,
                memories = state.memories,
                answer = state.answer,
                onMarkUnderstood = onMarkUnderstood,
                onMarkNeedsWork = onMarkNeedsWork,
                onAsk = onAsk,
                modifier = Modifier.padding(padding),
            )
        } else {
            when (selectedTab) {
                MainTab.School -> SchoolRouteScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Understand -> UnderstandingRouteScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Review -> ReviewScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    modifier = Modifier.padding(padding),
                )

                MainTab.Settings -> SettingsScreen(
                    state = state,
                    onReload = onReload,
                    onSelect = onSelect,
                    onSaveApiBaseUrl = onSaveApiBaseUrl,
                    onSaveAiModel = onSaveAiModel,
                    onCheckAi = onCheckAi,
                    modifier = Modifier.padding(padding),
                )
            }
        }
    }
}

@Composable
private fun TabIcon(tab: MainTab) {
    when (tab) {
        MainTab.School -> SchoolGlyph()
        MainTab.Understand -> RouteGlyph()
        MainTab.Review -> ReviewGlyph()
        MainTab.Settings -> SettingsGlyph()
    }
}

@Composable
private fun SchoolGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor),
        )
        Spacer(Modifier.height(3.dp))
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor.copy(alpha = 0.75f)),
        )
        Spacer(Modifier.height(3.dp))
        Box(
            modifier = Modifier
                .width(16.dp)
                .height(3.dp)
                .background(contentColor.copy(alpha = 0.5f)),
        )
    }
}

@Composable
private fun RouteGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
        Box(
            modifier = Modifier
                .width(2.dp)
                .height(8.dp)
                .background(contentColor.copy(alpha = 0.65f)),
        )
        Box(
            modifier = Modifier
                .size(6.dp)
                .clip(CircleShape)
                .background(contentColor),
        )
    }
}

@Composable
private fun ReviewGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        repeat(3) {
            Box(
                modifier = Modifier
                    .padding(vertical = 2.dp)
                    .width(16.dp)
                    .height(2.dp)
                    .background(contentColor),
            )
        }
    }
}

@Composable
private fun SettingsGlyph() {
    val contentColor = LocalContentColor.current

    Column(
        modifier = Modifier.size(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(3.dp, Alignment.CenterVertically),
    ) {
        SliderGlyphRow(dotOnLeft = false, color = contentColor)
        SliderGlyphRow(dotOnLeft = true, color = contentColor)
        SliderGlyphRow(dotOnLeft = false, color = contentColor.copy(alpha = 0.75f))
    }
}

@Composable
private fun SliderGlyphRow(dotOnLeft: Boolean, color: Color) {
    Row(
        modifier = Modifier.width(18.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(3.dp),
    ) {
        if (dotOnLeft) {
            Box(Modifier.size(5.dp).clip(CircleShape).background(color))
        }
        Box(
            modifier = Modifier
                .weight(1f)
                .height(2.dp)
                .background(color.copy(alpha = 0.7f)),
        )
        if (!dotOnLeft) {
            Box(Modifier.size(5.dp).clip(CircleShape).background(color))
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SchoolRouteScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    var query by rememberSaveable { mutableStateOf("") }
    var filter by rememberSaveable { mutableStateOf(TopicFilter.All) }
    val orderedTopics = state.topics.schoolOrdered()
    val gradeBuckets = orderedTopics.gradeBuckets()
    val gradeKeys = gradeBuckets.joinToString("|") { it.key }
    var selectedGradeKey by rememberSaveable { mutableStateOf<String?>(null) }
    val selectedGrade = gradeBuckets.firstOrNull { it.key == selectedGradeKey }
        ?: gradeBuckets.firstOrNull()
    val searchText = query.trim()
    val sourceTopics = if (searchText.isBlank()) {
        selectedGrade?.topics.orEmpty()
    } else {
        orderedTopics
    }
    val stepNumbers = sourceTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()
    val filteredTopics = sourceTopics.filter { topic ->
        val matchesQuery = searchText.isBlank() ||
            listOf(topic.name, topic.schoolPlace(), topic.human).any {
                it.contains(searchText, ignoreCase = true)
            }
        val matchesFilter = when (filter) {
            TopicFilter.All -> true
            TopicFilter.Open -> topic.id !in state.mastered
            TopicFilter.Mastered -> topic.id in state.mastered
        }
        matchesQuery && matchesFilter
    }

    LaunchedEffect(gradeKeys) {
        val keys = gradeBuckets.map { it.key }
        if (keys.isNotEmpty() && (selectedGradeKey == null || selectedGradeKey !in keys)) {
            selectedGradeKey = gradeBuckets.first().key
        }
    }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            SchoolHomeHeader(
                selectedGrade = selectedGrade?.label ?: "年级",
                total = state.topics.size,
                mastered = state.mastered.size,
            )
        }
        item {
            GradeSelector(
                buckets = gradeBuckets,
                selectedKey = selectedGrade?.key,
                onSelect = { selectedGradeKey = it },
            )
        }
        item {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                label = { Text("搜全部课本，比如 分数、方程") },
                leadingIcon = {
                    Icon(Icons.Filled.Search, contentDescription = null)
                },
                shape = CardShape,
            )
        }
        item {
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                TopicFilter.entries.forEach { option ->
                    FilterChip(
                        selected = filter == option,
                        onClick = { filter = option },
                        label = { Text(option.label) },
                    )
                }
            }
        }
        if (state.error != null) {
            item {
                ErrorPanel(message = state.error, onReload = onReload)
            }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) {
                LoadingTopicRow()
            }
        } else if (filteredTopics.isEmpty()) {
            item {
                EmptyPanel()
            }
        } else {
            items(filteredTopics, key = { it.id }) { topic ->
                CompactTopicRow(
                    step = stepNumbers.getValue(topic.id),
                    topic = topic,
                    mastered = topic.id in state.mastered,
                    primaryMeta = topic.schoolPlace(),
                    secondaryMeta = topic.human,
                ) {
                    onSelect(topic)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun UnderstandingRouteScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val orderedTopics = state.topics.understandingOrdered()
    val stepNumbers = orderedTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            RouteChoiceHeader(
                title = "按理解补：按先后顺序",
                body = "如果你不知道一个词到底是什么意思，走这条路。"
                    + "它先补更早需要懂的东西，再走到后面的正式说法。",
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else if (orderedTopics.isEmpty()) {
            item { EmptyPanel("暂无理解路线") }
        } else {
            item {
                SectionHeader(
                    title = "理解顺序",
                    meta = "${orderedTopics.count { it.id in state.mastered }}/${orderedTopics.size} 已经懂",
                )
            }
            items(orderedTopics, key = { "understand-${it.id}" }) { topic ->
                CompactTopicRow(
                    step = stepNumbers.getValue(topic.id),
                    topic = topic,
                    mastered = topic.id in state.mastered,
                    primaryMeta = topic.understandingPreview(),
                    secondaryMeta = "学校里通常在：${topic.schoolPlace()}",
                ) {
                    onSelect(topic)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun RouteChoiceHeader(
    title: String,
    body: String,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.primaryContainer,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                title,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                fontSize = 20.sp,
                fontWeight = FontWeight.SemiBold,
            )
            Text(
                body,
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 14.sp,
                lineHeight = 21.sp,
            )
        }
    }
}

@Composable
private fun ReviewScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    modifier: Modifier = Modifier,
) {
    val now = System.currentTimeMillis()
    val knownIds = state.topics.map { it.id }.toSet()
    val orderedTopics = state.topics.understandingOrdered()
    val stepNumbers = orderedTopics.mapIndexed { index, topic -> topic.id to index + 1 }.toMap()
    val openTopics = orderedTopics.filter { it.id !in state.mastered }
    val readyTopics = openTopics.filter { topic ->
        topic.prerequisites
            .filter { prerequisite -> prerequisite in knownIds }
            .all { prerequisite -> prerequisite in state.mastered }
    }
    val nextTopics = (readyTopics.ifEmpty { openTopics }).take(1)
    val masteredTopics = orderedTopics.filter { it.id in state.mastered }
    val dueTopics = masteredTopics.filter { topic ->
        state.memories[topic.id]?.isDue(now) == true
    }
    val laterTopics = masteredTopics.filter { topic -> topic !in dueTopics }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ProgressStrip(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        if (state.loading && state.topics.isEmpty()) {
            items(4) { LoadingTopicRow() }
        } else {
            item {
                SectionHeader(
                    title = "今天复习",
                    meta = "${dueTopics.size} 个到期",
                )
            }
            if (dueTopics.isEmpty()) {
                item { EmptyPanel("今天没有到期复习") }
            } else {
                items(dueTopics, key = { "due-${it.id}" }) { topic ->
                    CompactTopicRow(
                        step = stepNumbers.getValue(topic.id),
                        topic = topic,
                        mastered = true,
                        primaryMeta = state.memories[topic.id]?.memoryLine(now) ?: "现在复习",
                        secondaryMeta = topic.schoolPlace(),
                    ) {
                        onSelect(topic)
                    }
                }
            }

            item {
                SectionHeader(
                    title = "下一步",
                    meta = if (nextTopics.isEmpty()) {
                        "没有还没懂的知识"
                    } else {
                        "按理解顺序只给一个"
                    },
                )
            }
            if (nextTopics.isEmpty()) {
                item { EmptyPanel("暂无还没懂的知识") }
            } else {
                items(nextTopics, key = { "next-${it.id}" }) { topic ->
                    CompactTopicRow(
                        step = stepNumbers.getValue(topic.id),
                        topic = topic,
                        mastered = false,
                        primaryMeta = "下一步先学它",
                        secondaryMeta = topic.schoolPlace(),
                    ) {
                        onSelect(topic)
                    }
                }
            }

            item {
                SectionHeader(
                    title = "之后复习",
                    meta = "${laterTopics.size} 个知识点",
                )
            }
            if (laterTopics.isEmpty()) {
                item { EmptyPanel("还没有已经懂的记录") }
            } else {
                items(laterTopics, key = { "review-${it.id}" }) { topic ->
                    CompactTopicRow(
                        step = stepNumbers.getValue(topic.id),
                        topic = topic,
                        mastered = true,
                        primaryMeta = state.memories[topic.id]?.memoryLine(now)
                            ?: "复习时先问自己：我能用自己的话说出来吗？",
                        secondaryMeta = topic.schoolPlace(),
                    ) {
                        onSelect(topic)
                    }
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun SettingsScreen(
    state: UiState,
    onReload: () -> Unit,
    onSelect: (Topic) -> Unit,
    onSaveApiBaseUrl: (String) -> Unit,
    onSaveAiModel: (String) -> Unit,
    onCheckAi: (String, String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var apiBaseUrl by rememberSaveable(state.apiBaseUrl) {
        mutableStateOf(state.apiBaseUrl)
    }
    var aiModel by rememberSaveable(state.aiModel) {
        mutableStateOf(state.aiModel)
    }
    val orderedTopics = state.topics.understandingOrdered()
    val openTopics = orderedTopics.filter { it.id !in state.mastered }
    val nextTopic = openTopics.firstOrNull()
    val weakNames = nextTopic
        ?.prerequisites
        ?.filter { it !in state.mastered }
        ?.names(state.topics)
        .orEmpty()
    val dueCount = state.memories.values.count { it.isDue(System.currentTimeMillis()) }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            SettingsHeader(
                total = state.topics.size,
                mastered = state.mastered.size,
                loading = state.loading,
            )
        }
        if (state.error != null) {
            item { ErrorPanel(message = state.error, onReload = onReload) }
        }
        item {
            DetailPanel(title = "AI 老师") {
                OutlinedTextField(
                    value = apiBaseUrl,
                    onValueChange = { apiBaseUrl = it },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    label = { Text("后端地址和端口") },
                    shape = CardShape,
                )
                OutlinedTextField(
                    value = aiModel,
                    onValueChange = { aiModel = it },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    label = { Text("模型名称") },
                    shape = CardShape,
                )
                FlowRow(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.End),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Button(
                        onClick = { onSaveApiBaseUrl(apiBaseUrl) },
                        enabled = normalizeBaseUrl(apiBaseUrl) != state.apiBaseUrl,
                        shape = CardShape,
                    ) {
                        Text("保存并同步")
                    }
                    Button(
                        onClick = { onSaveAiModel(aiModel) },
                        enabled = aiModel.trim() != state.aiModel,
                        shape = CardShape,
                    ) {
                        Text("保存模型")
                    }
                    Button(
                        onClick = { onCheckAi(apiBaseUrl, aiModel) },
                        enabled = apiBaseUrl.isNotBlank(),
                        shape = CardShape,
                    ) {
                        Text("测试连接")
                    }
                }
                if (state.aiStatus.isNotBlank()) {
                    SettingRow("连接状态", state.aiStatus)
                }
                SettingRow(
                    "学习记忆",
                    "已懂 ${state.mastered.size} 个，记录 ${state.memories.size} 个，到期 $dueCount 个",
                )
                BodyText("问 AI 老师时，会把已会知识和可能薄弱的前置知识一起带上。")
                Button(
                    onClick = {
                        if (nextTopic != null) onSelect(nextTopic)
                    },
                    enabled = nextTopic != null,
                    shape = CardShape,
                ) {
                    Text("去问下一步知识")
                }
            }
        }
        item {
            DetailPanel(title = "个人知识地图") {
                SettingRow("已经懂", "${state.mastered.size} 个")
                SettingRow("到期复习", "$dueCount 个")
                SettingRow(
                    "还没懂",
                    "${(state.topics.size - state.mastered.size).coerceAtLeast(0)} 个",
                )
                SettingRow("下一步", nextTopic?.name ?: "暂无")
                SettingRow("可能先补", weakNames.ifBlank { "暂无" })
            }
        }
        item {
            DetailPanel(title = "内容范围") {
                SettingRow("内容来源", state.dataSource)
                SettingRow("当前可用", "${state.topics.size} 个知识点")
                SettingRow("覆盖方式", "按小学到初中主线、校内年级和理解依赖组织")
                if (state.syncWarning != null) {
                    BodyText("后端未同步，当前显示本机内容。")
                }
                BodyText(
                    "这不是完整教材章节点数量。"
                        + "后续需要继续按教材章、节、小节把骨架拆细。",
                )
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun SettingsHeader(
    total: Int,
    mastered: Int,
    loading: Boolean,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                "设置",
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 22.sp,
                fontWeight = FontWeight.SemiBold,
            )
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBlock(
                    label = if (loading) "同步中" else "知识点",
                    value = total.toString(),
                    modifier = Modifier.weight(1f),
                )
                MetricBlock(
                    label = "AI 记忆",
                    value = mastered.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.secondary,
                )
            }
        }
    }
}

@Composable
private fun SettingRow(
    label: String,
    value: String,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            label,
            modifier = Modifier.width(82.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 13.sp,
            lineHeight = 20.sp,
        )
        Text(
            value,
            modifier = Modifier.weight(1f),
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 15.sp,
            lineHeight = 22.sp,
        )
    }
}

@Composable
private fun SchoolHomeHeader(
    selectedGrade: String,
    total: Int,
    mastered: Int,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier.padding(14.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    "校内路线",
                    color = MaterialTheme.colorScheme.onSurface,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    "现在看：$selectedGrade",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            SmallTag("已懂 $mastered/$total")
        }
    }
}

@Composable
private fun GradeSelector(
    buckets: List<GradeBucket>,
    selectedKey: String?,
    onSelect: (String) -> Unit,
) {
    if (buckets.isEmpty()) return

    LazyRow(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        items(buckets, key = { it.key }) { bucket ->
            FilterChip(
                selected = bucket.key == selectedKey,
                onClick = { onSelect(bucket.key) },
                label = { Text("${bucket.label} ${bucket.topics.size}") },
            )
        }
    }
}

@Composable
private fun SectionHeader(
    title: String,
    meta: String,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 2.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.Bottom,
    ) {
        Text(
            title,
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 18.sp,
            fontWeight = FontWeight.SemiBold,
        )
        Text(
            meta,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ProgressStrip(
    total: Int,
    mastered: Int,
    loading: Boolean,
) {
    val open = (total - mastered).coerceAtLeast(0)
    val progress = if (total == 0) 0f else mastered.toFloat() / total.toFloat()

    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBlock(
                    label = if (loading) "同步中" else "全部",
                    value = total.toString(),
                    modifier = Modifier.weight(1f),
                )
                MetricBlock(
                    label = "已经懂",
                    value = mastered.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.secondary,
                )
                MetricBlock(
                    label = "还没懂",
                    value = open.toString(),
                    modifier = Modifier.weight(1f),
                    valueColor = MaterialTheme.colorScheme.tertiary,
                )
            }
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(8.dp)
                    .clip(PillShape)
                    .background(MaterialTheme.colorScheme.surfaceVariant),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(progress.coerceIn(0f, 1f))
                        .height(8.dp)
                        .background(MaterialTheme.colorScheme.primary),
                )
            }
        }
    }
}

@Composable
private fun MetricBlock(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
    valueColor: Color = MaterialTheme.colorScheme.onSurface,
) {
    Column(
        modifier = modifier,
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        Text(
            label,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
        Text(value, color = valueColor, fontSize = 24.sp, fontWeight = FontWeight.SemiBold)
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun CompactTopicRow(
    step: Int,
    topic: Topic,
    mastered: Boolean,
    primaryMeta: String,
    secondaryMeta: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Row(
            modifier = Modifier
                .clickable(onClick = onClick)
                .padding(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalAlignment = Alignment.Top,
        ) {
            Box(
                modifier = Modifier
                    .size(34.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    step.toString(),
                    color = MaterialTheme.colorScheme.primary,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.SemiBold,
                )
            }
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(3.dp),
            ) {
                Text(
                    topic.name.ifBlank { topic.id },
                    fontSize = 17.sp,
                    lineHeight = 22.sp,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    primaryMeta,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontSize = 13.sp,
                    lineHeight = 18.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    secondaryMeta,
                    color = MaterialTheme.colorScheme.primary,
                    fontSize = 13.sp,
                    lineHeight = 18.sp,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            StatusPill(mastered = mastered)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicRow(
    topic: Topic,
    mastered: Boolean,
    primaryMeta: String,
    secondaryMeta: String,
    onClick: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier
                .clickable(onClick = onClick)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Row(
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        primaryMeta,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp,
                        lineHeight = 20.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                    Text(
                        secondaryMeta,
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 13.sp,
                        lineHeight = 19.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
                StatusPill(mastered = mastered)
            }
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                SmallTag(topic.stageLabel())
                SmallTag("学它之前：${topic.prerequisites.size}个")
                SmallTag("以后会用：${topic.next.size}个")
            }
        }
    }
}

@Composable
private fun StatusPill(mastered: Boolean) {
    val container = if (mastered) {
        MaterialTheme.colorScheme.secondaryContainer
    } else {
        MaterialTheme.colorScheme.tertiaryContainer
    }
    val content = if (mastered) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.tertiary
    val label = if (mastered) "已经懂" else "还没懂"

    Surface(
        shape = PillShape,
        color = container,
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(7.dp)
                    .clip(CircleShape)
                    .background(content),
            )
            Text(label, color = content, fontSize = 12.sp, fontWeight = FontWeight.Medium)
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun TopicDetail(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    memories: Map<String, TopicMemory>,
    answer: String,
    onMarkUnderstood: (Topic) -> Unit,
    onMarkNeedsWork: (Topic) -> Unit,
    onAsk: suspend (Topic, String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var question by rememberSaveable(topic.id) { mutableStateOf("") }
    var asking by remember(topic.id) { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = ScreenPadding),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            DetailHeader(
                topic = topic,
                mastered = topic.id in mastered,
                memory = memories[topic.id],
                onMarkUnderstood = { onMarkUnderstood(topic) },
                onMarkNeedsWork = { onMarkNeedsWork(topic) },
            )
        }
        item {
            DetailPanel(title = "课本里在哪里") {
                BodyText(topic.schoolPlace())
            }
        }
        item {
            DetailPanel(title = "讲解") {
                ExplanationText(topic.explanationText())
            }
        }
        if (
            topic.conceptualLayers.isNotEmpty() ||
            topic.workedExamples.isNotEmpty() ||
            topic.practiceLadder.isNotEmpty() ||
            topic.reflectionQuestions.isNotEmpty()
        ) {
            item {
                DeepLearningPanel(topic = topic)
            }
        }
        item {
            DetailPanel(title = "关键词") {
                if (topic.terms.isEmpty()) {
                    BodyText("暂无")
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        topic.terms.entries.forEach { entry ->
                            TermRow(term = entry.key, explanation = entry.value)
                        }
                    }
                }
            }
        }
        item {
            LearningMap(
                topic = topic,
                topics = topics,
                mastered = mastered,
            )
        }
        item {
            DetailPanel(title = "误区与练习") {
                DenseTextBlock("容易错在", topic.misconceptions.ifEmpty { topic.defaultMisconceptions() })
                DenseTextBlock("练习方式", topic.exerciseTypes.ifEmpty { topic.defaultPractice() })
                if (topic.visuals.isNotEmpty()) {
                    DenseTextBlock("辅助表示", topic.visuals)
                }
            }
        }
        item {
            DetailPanel(title = "问 AI 老师") {
                AIMemoryNote(topic = topic, topics = topics, mastered = mastered, memories = memories)
                OutlinedTextField(
                    value = question,
                    onValueChange = { question = it },
                    modifier = Modifier.fillMaxWidth(),
                    minLines = 3,
                    label = { Text("卡住的词、步骤或题目") },
                    enabled = !asking,
                    shape = CardShape,
                )
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End,
                ) {
                    Button(
                        onClick = {
                            val submitted = question.trim()
                            if (submitted.isNotEmpty()) {
                                scope.launch {
                                    asking = true
                                    onAsk(topic, submitted)
                                    asking = false
                                }
                            }
                        },
                        enabled = question.isNotBlank() && !asking,
                        shape = CardShape,
                    ) {
                        if (asking) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                color = MaterialTheme.colorScheme.onPrimary,
                                strokeWidth = 2.dp,
                            )
                            Spacer(Modifier.width(8.dp))
                        }
                        Text("问老师")
                    }
                }
                if (answer.isNotBlank()) {
                    AnswerBubble(answer = answer)
                }
            }
        }
        item { Spacer(Modifier.height(12.dp)) }
    }
}

@Composable
private fun DeepLearningPanel(topic: Topic) {
    DetailPanel(title = "深度理解") {
        DenseTextBlock("分层解释", topic.conceptualLayers)
        topic.workedExamples.forEach { example ->
            WorkedExampleBlock(example)
        }
        if (topic.practiceLadder.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("练习阶梯", fontSize = 13.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                topic.practiceLadder.forEach { task ->
                    PracticeTaskRow(task)
                }
            }
        }
        DenseTextBlock("自查问题", topic.reflectionQuestions)
    }
}

@Composable
private fun WorkedExampleBlock(example: WorkedExample) {
    Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
        Text(example.title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        BodyText(example.problem)
        example.steps.forEachIndexed { index, step ->
            BodyText("${index + 1}. $step")
        }
        if (example.answerCheck.isNotBlank()) {
            BodyText("检查：${example.answerCheck}")
        }
    }
}

@Composable
private fun PracticeTaskRow(task: PracticeTask) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(task.level, fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
        BodyText(task.prompt)
        BodyText("目标：${task.goal}")
    }
}

@Composable
private fun AIMemoryNote(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
    memories: Map<String, TopicMemory>,
) {
    val known = topic.prerequisites.names(topics, onlyMastered = mastered)
    val weak = topic.prerequisites.names(topics, excludeMastered = mastered)
    val dueCount = memories.values.count { it.isDue(System.currentTimeMillis()) }

    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        SmallTag("会参考已懂记录：${mastered.size} 个")
        SmallTag("到期复习：$dueCount 个")
        MapRow("本题前面已经会", known)
        MapRow("本题前面可能要补", weak)
    }
}

@Composable
private fun DetailHeader(
    topic: Topic,
    mastered: Boolean,
    memory: TopicMemory?,
    onMarkUnderstood: () -> Unit,
    onMarkNeedsWork: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.Top,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        topic.name.ifBlank { topic.id },
                        fontSize = 26.sp,
                        lineHeight = 32.sp,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        topic.human,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 15.sp,
                        lineHeight = 22.sp,
                    )
                    if (memory != null) {
                        Text(
                            memory.memoryLine(System.currentTimeMillis()),
                            color = MaterialTheme.colorScheme.primary,
                            fontSize = 13.sp,
                            lineHeight = 19.sp,
                        )
                    }
                }
                SmallTag(topic.stageLabel())
            }
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                StatusPill(mastered = mastered)
                Spacer(Modifier.weight(1f))
                Button(onClick = onMarkNeedsWork, shape = CardShape) {
                    Text("我还没懂")
                }
                Button(onClick = onMarkUnderstood, shape = CardShape) {
                    Text(if (mastered) "复习完成" else "我懂了")
                }
            }
        }
    }
}

@Composable
private fun LearningMap(
    topic: Topic,
    topics: List<Topic>,
    mastered: Set<String>,
) {
    DetailPanel(title = "学它前后要知道什么") {
        MapRow("已经会的旧知识", topic.prerequisites.names(topics, onlyMastered = mastered))
        MapRow("可能要先补的旧知识", topic.prerequisites.names(topics, excludeMastered = mastered))
        MapRow("以后会用到它的知识", topic.next.names(topics))
    }
}

@Composable
private fun RouteLine(
    label: String,
    steps: List<String>,
) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(label, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
        BodyText(steps.joinToString(" -> "))
    }
}

@Composable
private fun DetailPanel(
    title: String,
    content: @Composable ColumnScope.() -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                title,
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 16.sp,
                fontWeight = FontWeight.SemiBold,
            )
            content()
        }
    }
}

@Composable
private fun MapRow(label: String, value: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text(value, fontSize = 15.sp, lineHeight = 22.sp, color = MaterialTheme.colorScheme.onSurface)
    }
}

@Composable
private fun DenseTextBlock(
    label: String,
    values: List<String>,
) {
    if (values.isEmpty()) return

    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(label, fontSize = 13.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
        BodyText(values.joinToString("；") + "。")
    }
}

@Composable
private fun ExplanationText(value: String) {
    BodyText(value)
}

@Composable
private fun TermRow(term: String, explanation: String) {
    Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
        Text(term, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
        BodyText(explanation)
    }
}

@Composable
private fun RouteStep(index: Int, value: String) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Box(
            modifier = Modifier
                .size(28.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer),
            contentAlignment = Alignment.Center,
        ) {
            Text(index.toString(), color = MaterialTheme.colorScheme.primary, fontSize = 12.sp)
        }
        BodyText(value, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun AnswerBubble(answer: String) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.secondaryContainer,
    ) {
        Text(
            answer,
            modifier = Modifier.padding(14.dp),
            color = MaterialTheme.colorScheme.onSurface,
            fontSize = 15.sp,
            lineHeight = 23.sp,
        )
    }
}

@Composable
private fun BodyText(
    value: String,
    modifier: Modifier = Modifier,
) {
    Text(
        value,
        modifier = modifier,
        color = MaterialTheme.colorScheme.onSurface,
        fontSize = 15.sp,
        lineHeight = 23.sp,
    )
}

@Composable
private fun SmallTag(value: String) {
    Surface(
        shape = PillShape,
        color = MaterialTheme.colorScheme.surfaceVariant,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            value,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontSize = 12.sp,
            fontWeight = FontWeight.Medium,
        )
    }
}

@Composable
private fun ErrorPanel(
    message: String,
    onReload: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = Color(0xFFFFF1F0),
        border = BorderStroke(1.dp, Color(0xFFFFDAD6)),
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("同步失败", color = Color(0xFFB42318), fontWeight = FontWeight.SemiBold)
                Text(message, color = Color(0xFF8C1D18), fontSize = 13.sp, maxLines = 2)
            }
            Button(onClick = onReload, shape = CardShape) {
                Text("重试")
            }
        }
    }
}

@Composable
private fun EmptyPanel(message: String = "没有匹配结果") {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Text(
            message,
            modifier = Modifier.padding(18.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun LoadingTopicRow() {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = CardShape,
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            LoadingBar(width = 0.42f, height = 18.dp)
            LoadingBar(width = 0.88f, height = 14.dp)
            LoadingBar(width = 0.55f, height = 14.dp)
        }
    }
}

@Composable
private fun LoadingBar(width: Float, height: androidx.compose.ui.unit.Dp) {
    Box(
        modifier = Modifier
            .fillMaxWidth(width)
            .height(height)
            .clip(PillShape)
            .background(MaterialTheme.colorScheme.surfaceVariant),
    )
}

private fun List<String>.names(
    topics: List<Topic>,
    onlyMastered: Set<String>? = null,
    excludeMastered: Set<String>? = null,
): String {
    val names = filter {
        (onlyMastered == null || it in onlyMastered) &&
            (excludeMastered == null || it !in excludeMastered)
    }.map { id -> topics.firstOrNull { it.id == id }?.name ?: id }
    return names.joinToString("、").ifBlank { "暂无" }
}

private fun Topic.stageLabel(): String = when (gradeBand) {
    "primary" -> "小学会学"
    "junior" -> "初中会学"
    "primary_to_junior" -> "小初衔接会用"
    else -> gradeBand.ifBlank { "校内知识" }
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

private fun Topic.understandingPreview(): String {
    val steps = route.take(4)
    return if (steps.isEmpty()) {
        "入口：" + human.ifBlank { name }
    } else {
        "顺序：${steps.joinToString(" -> ")}"
    }
}

private fun Topic.explanationText(): String {
    val paragraphs = mutableListOf<String>()
    if (human.isNotBlank()) {
        paragraphs += human
    }
    if (why.isNotBlank()) {
        paragraphs += why
    }
    if (lifeExamples.isNotEmpty()) {
        paragraphs += "可以把它放到这些场景里看：${lifeExamples.joinToString("、")}。"
    }
    if (route.isNotEmpty()) {
        paragraphs += "理解顺序是：${route.joinToString("，然后")}。"
    }
    if (conceptualLayers.isNotEmpty()) {
        paragraphs += "先分层理解：${conceptualLayers.joinToString(" ")}"
    }
    val definition = formalDefinition.ifBlank { human }
    if (definition.isNotBlank() && definition != human) {
        paragraphs += "课本里的正式说法是：$definition"
    }
    if (formulas.isNotEmpty()) {
        paragraphs += "常见写法：${formulas.joinToString("，")}。"
    }
    return paragraphs.joinToString("\n\n").ifBlank { "暂无讲解" }
}

private fun Topic.defaultMisconceptions(): List<String> = listOf(
    "只记住说法或公式，但说不出它表示什么。",
    "能做熟题，换一种问法就不知道该怎样判断。",
)

private fun Topic.defaultPractice(): List<String> = listOf(
    "用自己的话讲一遍这个知识点。",
    "举一个例子，并说清楚例子里的数量或图形关系。",
    "做题前先说清楚已知什么、要求什么、该用哪个关系。",
)

private fun List<Topic>.schoolOrdered(): List<Topic> = mapIndexed { index, topic -> index to topic }
    .sortedWith(
        compareBy<Pair<Int, Topic>> { it.second.textbookPositions.firstOrNull()?.grade.gradeOrder() }
            .thenBy { it.second.textbookPositions.firstOrNull()?.chapter.chapterOrder() }
            .thenBy { it.first },
    )
    .map { it.second }

private fun List<Topic>.gradeBuckets(): List<GradeBucket> {
    val order = listOf(
        "一年级",
        "二年级",
        "三年级",
        "四年级",
        "五年级",
        "六年级",
        "七年级",
        "八年级",
        "九年级",
        "小学",
        "初中",
        "其他",
    )
    val grouped = groupBy { it.schoolGradeKey() }
    return order.mapNotNull { key ->
        grouped[key]?.let { topics ->
            GradeBucket(key = key, label = key, topics = topics)
        }
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
        gradeBand == "primary" -> "小学"
        gradeBand == "junior" -> "初中"
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
        '一' to 1,
        '二' to 2,
        '三' to 3,
        '四' to 4,
        '五' to 5,
        '六' to 6,
        '七' to 7,
        '八' to 8,
        '九' to 9,
        '十' to 10,
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
    mastered: Set<String>,
    memories: List<TopicMemory>,
): String =
    withContext(Dispatchers.IO) {
        val body = JSONObject()
            .put("age", 12)
            .put("question", question)
            .put("model", model.trim())
            .put("mastered", JSONArray(mastered.sorted()))
            .put("memories", memories.sortedBy { it.topicId }.toRequestJsonArray())
        JSONObject(post(baseUrl, "/topics/$topicId/teacher-answer", body.toString()))
            .optString("answer")
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
            !backendOk -> "后端异常"
            !hasKey -> "后端缺少 OPENAI_API_KEY"
            !hasModel -> "请填写模型名称"
            else -> "AI 可用：$selectedModel"
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
    if (!isMastered) return "已记录：这里还不稳，复习页会继续排它。"
    val due = nextReviewAt ?: return "已记录：还没有下次复习时间。"
    val remaining = due - now
    val days = ((remaining + DAY_MS - 1) / DAY_MS).toInt()
    return when {
        remaining <= 0 -> "已记录：现在该复习。复习次数 $reviewCount 次。"
        days <= 1 -> "已记录：约 1 天后复习。复习次数 $reviewCount 次。"
        else -> "已记录：约 $days 天后复习。复习次数 $reviewCount 次。"
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
