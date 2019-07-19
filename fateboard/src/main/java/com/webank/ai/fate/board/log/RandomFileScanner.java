package com.webank.ai.fate.board.log;

import com.alibaba.fastjson.JSON;
import com.google.common.collect.Lists;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.websocket.Session;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

public class RandomFileScanner implements Runnable, LogScanner {

    private static final Logger logger = LoggerFactory.getLogger(RandomFileScanner.class);

    public RandomFileScanner(File file, Session session, long skipLine) {

        try {
            tailFile = new TailFile(file, 0);
        } catch (IOException e) {
            logger.error("init RandomFileScanner failed", e);

        }
        this.session = session;
        this.skipLine = skipLine;
    }

    long skipLine;

    TailFile tailFile;

    long flushNum;

    Session session;

    public TailFile getTailFile() {
        return tailFile;
    }

    public void setTailFile(TailFile tailFile) {
        this.tailFile = tailFile;
    }

    public Session getSession() {
        return session;
    }

    public void setSession(Session session) {
        this.session = session;
    }

    @Override
    public boolean isNeedStop() {
        return needStop;
    }

    @Override
    public void setNeedStop(boolean needStop) {
        this.needStop = needStop;
    }

    boolean needStop = false;

    @Override
    public void run() {
        try {
            while (true) {

                try {
                    if (needStop) {
                        logger.info("roll file thread return");
                        return;
                    }
                    //List<String> lines = tailFile.readEvents(100);
                    List<Map> lines  = tailFile.readEventMap(100);

                    if (lines == null) {
                        throw new Exception("lines not exist");
                    }
                    if (lines.size() == 0) {
//                        if(session.isOpen())
//                        {
//                            session.getBasicRemote().flushBatch();
//                        }

                        Thread.sleep(500);


                    } else {
                        List<Map>  result = Lists.newArrayList();
                        lines.forEach(content -> {

                            flushNum++;
                            if (session.isOpen()) {

                                    if (flushNum > skipLine) {

                                      //  session.getBasicRemote().sendText(content);
                                        result.add(content);

                                    }

                            } else {
                                needStop = true;
                                return ;
                            }

                        });

                        if(session.isOpen())
                        {
                            session.getBasicRemote().sendText(JSON.toJSONString(result));
                           // session.getBasicRemote().flushBatch();
                        }


                    }
                } catch (Exception e) {
                    logger.error("roll local file error", e);
                }
            }
        } finally {
            if (tailFile != null) {
                tailFile.close();
            }
        }

    }
}
